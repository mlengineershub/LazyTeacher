# Dockerfile for deploying LazyTeacher api in a container
# Authors: Ilan ALIOUCHOUCHE & Ilyes DJERFAF

FROM nginx:alpine

COPY app/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]