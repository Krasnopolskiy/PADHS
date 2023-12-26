FROM alpine:latest

RUN apk add --no-cache gcc musl-dev

WORKDIR /app

COPY benchmark.c .

RUN gcc benchmark.c -o benchmark

CMD ["./benchmark"]
