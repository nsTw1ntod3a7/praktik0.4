using System;
using System.Collections.Generic;

namespace GradeCalculationApp
{
    /// <summary>
    /// Точка входа консольного приложения.
    /// Запускает серию тестов для проверки работы калькулятора среднего балла.
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Тестирование калькулятора среднего балла ===\n");

            // Набор тестовых данных для сверки результатов после рефакторинга
            RunTest("Обычный набор оценок", new List<int> { 4, 5, 3, 4, 5 });
            RunTest("Список с невалидными значениями", new List<int> { 1, 6, 4, 0, 3 });
            RunTest("Пустой список", new List<int>());
            RunTest("Null вместо списка", null);
            RunTest("Одна корректная оценка", new List<int> { 5 });

            Console.WriteLine("\n=== Тесты завершены ===");
            Console.WriteLine("Нажмите любую клавишу для выхода...");
            Console.ReadKey();
        }

        /// <summary>
        /// Вспомогательный метод для вывода результатов теста в консоль.
        /// </summary>
        static void RunTest(string testName, List<int> data)
        {
            string inputStr = data == null ? "null" : string.Join(", ", data);
            Console.WriteLine($"{testName}");
            Console.WriteLine($"   Вход: [{inputStr}]");
            Console.WriteLine($"   → {GradeCalculator.CalculateAverage(data)}");
            Console.WriteLine();
        }
    }

    /// <summary>
    /// Класс для расчёта среднего балла.
    /// Принимает список целых чисел, отбирает только допустимые оценки,
    /// вычисляет среднее арифметическое и возвращает отформатированную строку.
    /// </summary>
    public class GradeCalculator
    {
        /// <summary>Минимальная допустимая оценка.</summary>
        private const int MinGrade = 2;

        /// <summary>Максимальная допустимая оценка.</summary>
        private const int MaxGrade = 5;

        /// <summary>
        /// Основной метод: проверяет входные данные, вызывает расчёт и форматирование.
        /// </summary>
        /// <param name="grades">Список оценок</param>
        /// <returns>Строка с результатом или сообщением об ошибке</returns>
        public static string CalculateAverage(List<int> grades)
        {
            if (grades == null)
            {
                return "ОШИБКА: входные данные отсутствуют";
            }
            if (grades.Count == 0)
            {
                return "ОШИБКА: список оценок пуст";
            }

            int validCount;
            string inputLog;
            double avg = CalculateAverageValue(grades, out validCount, out inputLog);

            if (validCount == 0)
            {
                return $"ОШИБКА: не найдено валидных оценок ({MinGrade}-{MaxGrade})";
            }

            return FormatResult(inputLog, avg);
        }

        /// <summary>
        /// Расчёт: считает среднее арифметическое по допустимым оценкам.
        /// </summary>
        /// <param name="grades">Список оценок</param>
        /// <param name="validCount">Количество допустимых оценок</param>
        /// <param name="inputLog">Строка со всеми входными значениями</param>
        /// <returns>Среднее значение (0, если допустимых оценок нет)</returns>
        private static double CalculateAverageValue(List<int> grades, out int validCount, out string inputLog)
        {
            int sum = 0;
            validCount = 0;
            inputLog = "";

            foreach (int grade in grades)
            {
                if (grade >= MinGrade && grade <= MaxGrade)
                {
                    sum = sum + grade;
                    validCount = validCount + 1;
                }

                // Фиксируем каждое входное значение в лог-строке
                inputLog = inputLog + grade.ToString() + ", ";
            }

            if (validCount == 0)
            {
                return 0;
            }

            return (double)sum / validCount;
        }

        /// <summary>
        /// Форматирование: собирает итоговую строку.
        /// </summary>
        private static string FormatResult(string inputLog, double avg)
        {
            return "Оценки: " + inputLog.TrimEnd(',', ' ') + " | Средний балл: " + avg.ToString("F2");
        }
    }
}
