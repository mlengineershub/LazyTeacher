from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
    Literal
)

if TYPE_CHECKING:
    from transformers import (
        FeatureExtractionMixin,
        Pipeline,
        PreTrainedModel,
        PreTrainedTokenizer,
        TFPreTrainedModel
    )

from datasets import Dataset

from evaluate.evaluator.text_classification import (
    TextClassificationEvaluator,
    add_end_docstrings,
    add_start_docstrings,
    EvaluationModule,
    Number,
    TASK_DOCUMENTATION
)

from evaluate.evaluator.base import (
    load,
    EVALUTOR_COMPUTE_START_DOCSTRING,
    EVALUATOR_COMPUTE_RETURN_DOCSTRING
)


class TextMultiClassificationEvaluator(TextClassificationEvaluator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute_metric(
        self,
        metric: List[Tuple[EvaluationModule, Dict[str, Any]]],
        metric_inputs: Dict,
        strategy: Literal["simple", "bootstrap"] = "simple",
        confidence_level: float = 0.95,
        n_resamples: int = 9999,
        random_state: Optional[int] = None,
        metrics_kwargs: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Compute and return metrics."""
        if isinstance(metric, list):
            if strategy == "bootstrap":
                raise ValueError("Bootstrap strategy is not supported "
                                 "with multiple metrics.")
            result = {}
            for m, kwarg in metric:
                result_m = self.compute_metric(m,
                                               metric_inputs,
                                               strategy,
                                               confidence_level,
                                               n_resamples,
                                               random_state,
                                               kwarg)
                result.update({f"{m}_{k}_{v}": result_m.values()
                              for k, v in kwarg.items()})

        result = metric.compute(
            **metric_inputs,
            **metrics_kwargs
        )
        if strategy == "bootstrap":
            metric_keys = result.keys()
            bootstrap_dict = self._compute_confidence_interval(
                metric,
                metric_inputs,
                metric_keys,
                confidence_level,
                n_resamples,
                random_state,
            )
            for key in metric_keys:
                bootstrap_dict[key]["score"] = result[key]
            return bootstrap_dict
        return result

    def prepare_metric(
        self,
        metric: Union[str, EvaluationModule,
                      List[str], List[EvaluationModule]],
        metrics_kwargs: Optional[Dict[str, Union[Dict, List]]] = None
    ) -> List[Tuple[EvaluationModule, Dict[str, Any]]]:
        """
        Prepare metric.
        Args:
            metric (`str` or `EvaluationModule` or `List[str]`
                    or `List[EvaluationModule]`):
                Specifies the metric we use in evaluator.
                If it is of type `str`, we treat it as the metric name, and
                load it. Otherwise we assume it represents a pre-loaded metric.
        Returns:
            The loaded metric.
        Example:
        ```py
        >>> from evaluate import evaluator
        >>> evaluator("text-classification").prepare_metric("accuracy")
        ```
        """
        # Prepare metric.
        if metric is None:
            if self.default_metric_name is None:
                raise ValueError(
                    "`Evaluator` doesn't specify a default metric. "
                    "Please specify a valid `metric` argument."
                )
            metric = load(self.default_metric_name)
        elif isinstance(metric, str):
            if metrics_kwargs and metric in metrics_kwargs:
                if isinstance(metrics_kwargs[metric], dict):
                    return [(load(metric), metrics_kwargs[metric])]
                elif isinstance(metrics_kwargs[metric], list):
                    return [(load(metric), m) for m in metrics_kwargs[metric]]
            return [(load(metric), {})]
        elif isinstance(metric, EvaluationModule):
            return [(metric, {})]
        elif isinstance(metric, list):
            metric_ = []
            for m in metric:
                if isinstance(m, str):
                    m = load(m)
                if metrics_kwargs and m in metrics_kwargs:
                    if isinstance(metrics_kwargs[m], dict):
                        metric_.append((m, metrics_kwargs[m]))
                    elif isinstance(metrics_kwargs[m], list):
                        metric_.extend([(m, m_)
                                        for m_ in metrics_kwargs[m]])
                if not metrics_kwargs or m not in metrics_kwargs:
                    metric_.append((m, {}))

            return metric_

    @add_start_docstrings(EVALUTOR_COMPUTE_START_DOCSTRING)
    @add_end_docstrings(EVALUATOR_COMPUTE_RETURN_DOCSTRING, TASK_DOCUMENTATION)
    def compute(
        self,
        model_or_pipeline: Union[
            str, "Pipeline", Callable, "PreTrainedModel",  # noqa: F821
            "TFPreTrainedModel"
        ] = None,
        data: Union[str, Dataset] = None,
        subset: Optional[str] = None,
        split: Optional[str] = None,
        metric: Union[str, EvaluationModule,
                      List[str], List[EvaluationModule]] = None,
        tokenizer: Optional[Union[str,  # noqa: F821
                                  "PreTrainedTokenizer"]] = None,
        feature_extractor: Optional[Union[str,  # noqa: F821
                                          "FeatureExtractionMixin"]] = None,
        strategy: Literal["simple", "bootstrap"] = "simple",
        confidence_level: float = 0.95,
        n_resamples: int = 9999,
        device: int = None,
        random_state: Optional[int] = None,
        input_column: str = "text",
        second_input_column: Optional[str] = None,
        label_column: str = "label",
        label_mapping: Optional[Dict[str, Number]] = None,
        metrics_kwargs: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, float], Any]:
        """
        input_column (`str`, *optional*, defaults to `"text"`):
            The name of the column containing the text feature
            in the dataset specified by `data`.
        second_input_column (`str`, *optional*, defaults to `None`):
            The name of the second column containing the text features.
            This may be useful for classification tasks
            as MNLI, where two columns are used.
        label_column (`str`, defaults to `"label"`):
            The name of the column containing the labels in the dataset
            specified by `data`.
        label_mapping (`Dict[str, Number]`, *optional*, defaults to `None`):
            We want to map class labels defined by the model
            in the pipeline to values consistent with those
            defined in the `label_column` of the `data` dataset.
        metrics_kwargs (`Dict[str, Any]`, *optional*, defaults to `None`):
            Additional keyword to pass to the metric(s).
        """
        result = {}
        self.check_for_mismatch_in_device_setup(device, model_or_pipeline)
        # Prepare inputs
        data = self.load_data(data=data, subset=subset, split=split)
        metric_inputs, pipe_inputs = self.prepare_data(
            data=data, input_column=input_column,
            second_input_column=second_input_column, label_column=label_column
        )
        pipe = self.prepare_pipeline(
            model_or_pipeline=model_or_pipeline,
            tokenizer=tokenizer,
            feature_extractor=feature_extractor,
            device=device,
        )
        metric = self.prepare_metric(metric)
        # Compute predictions
        predictions, perf_results = self.call_pipeline(pipe, pipe_inputs)
        predictions = self.predictions_processor(predictions, label_mapping)
        metric_inputs.update(predictions)
        # Compute metrics from references and predictions
        metric_results = self.compute_metric(
            metric=metric,
            metric_inputs=metric_inputs,
            strategy=strategy,
            confidence_level=confidence_level,
            n_resamples=n_resamples,
            random_state=random_state,
            metrics_kwargs=metrics_kwargs
        )
        result.update(metric_results)
        result.update(perf_results)

        return result
