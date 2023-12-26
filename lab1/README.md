# НИЯУ МИФИ. Лабораторная работа №1. Краснопольский Иван, Б21-525. 2023

## Описание бенчмарка

Переменная `count` увеличивается на 1 в очень длинном цикле.

## Вычисления

- Хост-машина

  ```text
  The task took 50.311000 seconds to execute.
  ```

- Контейнер

  ```text
  The task took 56.860005 seconds to execute.
  ```

## Заключение

В ходе лабораторной работы был проведен бенчмарк для оценки производительности вычислительных операций на хост-машине и
внутри контейнера Docker. Результаты показали, что задача на хост-машине выполнялась быстрее, чем задача в Docker
контейнере. Это указывает на то, что хост-машина обладает лучшей производительностью по сравнению с выполнением той же
задачи в контейнеризированной среде. Такое различие во времени выполнения может быть обусловлено дополнительными
накладными расходами, включая управление ресурсами и изоляцию процессов.

## Приложение

### Бенчмарк

<details>
  <summary>Исходный код</summary>

```c++
#include <stdio.h>
#include <time.h>

void benchmark() {
    long long count = 0;
    for (long long i = 0; i < 20000000000; i++) { count++; }
}

int main() {
    clock_t start, end;
    double cpu_time_used;

    start = clock();
    benchmark();
    end = clock();

    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;

    printf("The task took %f seconds to execute.\n", cpu_time_used);

    return 0;
}
```

</details>


### Dockerfile

<details>
  <summary>Исходный код</summary>

```dockerfile
FROM alpine:latest

RUN apk add --no-cache gcc musl-dev

WORKDIR /app

COPY benchmark.c .

RUN gcc benchmark.c -o benchmark

CMD ["./benchmark"]
```

</details>