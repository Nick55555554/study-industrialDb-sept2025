using Microsoft.Maui.Controls;

namespace IndustrialDbWorkingFrontend
{
    public partial class MainPage : ContentPage
    {
        private int currentColumnCount = 0;
        private int currentRowCount = 0;

        public MainPage()
        {
            InitializeComponent();
        }

        private void OnCreateTableClicked(object sender, EventArgs e)
        {
            CreateTable();
        }

        private void OnAddColumnClicked(object sender, EventArgs e)
        {
            AddColumn();
        }

        private void OnDeleteColumnClicked(object sender, EventArgs e)
        {
            DeleteColumn();
        }

        private void OnAddRowClicked(object sender, EventArgs e)
        {
            AddRow();
        }

        private void UpdateButtonsState()
        {
            bool hasTable = currentColumnCount > 0 && currentRowCount > 0;
            AddColumnBtn.IsEnabled = hasTable;
            DeleteColumnBtn.IsEnabled = hasTable && currentColumnCount > 1;
            AddRowBtn.IsEnabled = hasTable;
        }

        private void CreateTable()
        {
            if (!int.TryParse(ColumnCountEntry.Text, out int columns) || 
                !int.TryParse(RowCountEntry.Text, out int rows))
            {
                DisplayAlert("Ошибка", "Введите корректные числа", "OK");
                return;
            }

            if (columns <= 0 || rows <= 0)
            {
                DisplayAlert("Ошибка", "Количество столбцов и строк должно быть больше 0", "OK");
                return;
            }

            // Очищаем предыдущую таблицу
            MainTableGrid.Children.Clear();
            MainTableGrid.ColumnDefinitions.Clear();
            MainTableGrid.RowDefinitions.Clear();

            // Создаем колонки
            for (int i = 0; i < columns; i++)
            {
                MainTableGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Star });
            }

            // Создаем строки
            for (int i = 0; i < rows; i++)
            {
                MainTableGrid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
            }

            // Создаем заголовки столбцов
            for (int col = 0; col < columns; col++)
            {
                var headerLabel = new Label
                {
                    Text = $"Столбец {col + 1}",
                    BackgroundColor = Color.FromArgb("#007ACC"),
                    TextColor = Colors.White,
                    HorizontalOptions = LayoutOptions.Fill,
                    VerticalOptions = LayoutOptions.Fill,
                    HorizontalTextAlignment = TextAlignment.Center,
                    VerticalTextAlignment = TextAlignment.Center,
                    Padding = new Thickness(10),
                    FontAttributes = FontAttributes.Bold
                };
                MainTableGrid.Add(headerLabel, col, 0);
            }

            // Создаем ячейки таблицы
            for (int row = 1; row < rows; row++)
            {
                for (int col = 0; col < columns; col++)
                {
                    var entry = new Entry
                    {
                        Text = $"Данные {row},{col + 1}",
                        BackgroundColor = row % 2 == 1 ? Color.FromArgb("#f8f9fa") : Colors.White,
                        TextColor = Colors.Black,
                        Placeholder = $"Введите данные",
                        ClearButtonVisibility = ClearButtonVisibility.WhileEditing
                    };

                    var border = new Border
                    {
                        Content = entry,
                        Stroke = Color.FromArgb("#dee2e6"),
                        StrokeThickness = 1,
                        BackgroundColor = Colors.Transparent,
                        Padding = new Thickness(5)
                    };

                    MainTableGrid.Add(border, col, row);
                }
            }

            currentColumnCount = columns;
            currentRowCount = rows - 1; // -1 потому что первая строка - заголовки

            TableBorder.IsVisible = true;
            NoTableLabel.IsVisible = false;
            UpdateButtonsState();
        }

        private void AddColumn()
        {
            if (currentColumnCount == 0) return;

            currentColumnCount++;
            int newColIndex = currentColumnCount - 1;

            // Добавляем новую колонку
            MainTableGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Star });

            // Заголовок нового столбца
            var headerLabel = new Label
            {
                Text = $"Столбец {currentColumnCount}",
                BackgroundColor = Color.FromArgb("#007ACC"),
                TextColor = Colors.White,
                HorizontalOptions = LayoutOptions.Fill,
                VerticalOptions = LayoutOptions.Fill,
                HorizontalTextAlignment = TextAlignment.Center,
                VerticalTextAlignment = TextAlignment.Center,
                Padding = new Thickness(10),
                FontAttributes = FontAttributes.Bold
            };
            MainTableGrid.Add(headerLabel, newColIndex, 0);

            // Ячейки нового столбца
            for (int row = 1; row <= currentRowCount; row++)
            {
                var entry = new Entry
                {
                    Text = $"Новые {row},{currentColumnCount}",
                    BackgroundColor = row % 2 == 1 ? Color.FromArgb("#f8f9fa") : Colors.White,
                    TextColor = Colors.Black,
                    Placeholder = $"Введите данные"
                };

                var border = new Border
                {
                    Content = entry,
                    Stroke = Color.FromArgb("#dee2e6"),
                    StrokeThickness = 1,
                    BackgroundColor = Colors.Transparent,
                    Padding = new Thickness(5)
                };

                MainTableGrid.Add(border, newColIndex, row);
            }

            UpdateButtonsState();
        }

        private void DeleteColumn()
        {
            if (currentColumnCount <= 1) return;

            int colToRemove = currentColumnCount - 1;

            // Создаем список для удаления (чтобы избежать изменения коллекции во время итерации)
            var childrenToRemove = new List<IView>();

            // Находим элементы для удаления
            foreach (var child in MainTableGrid.Children)
            {
                if (GetGridColumn(child) == colToRemove)
                {
                    childrenToRemove.Add(child);
                }
            }

            // Удаляем элементы
            foreach (var child in childrenToRemove)
            {
                MainTableGrid.Children.Remove(child);
            }

            // Удаляем колонку из определений
            if (MainTableGrid.ColumnDefinitions.Count > colToRemove)
            {
                MainTableGrid.ColumnDefinitions.RemoveAt(colToRemove);
            }
            
            currentColumnCount--;
            UpdateButtonsState();
        }

        // Исправленные методы для получения позиций в Grid
        private int GetGridColumn(IView view)
        {
            if (view is BindableObject bindable)
            {
                return Grid.GetColumn(bindable);
            }
            return 0;
        }

        private int GetGridRow(IView view)
        {
            if (view is BindableObject bindable)
            {
                return Grid.GetRow(bindable);
            }
            return 0;
        }

        private void AddRow()
        {
            if (currentColumnCount == 0) return;

            currentRowCount++;
            int newRowIndex = currentRowCount;

            // Добавляем новую строку
            MainTableGrid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });

            // Ячейки новой строки
            for (int col = 0; col < currentColumnCount; col++)
            {
                var entry = new Entry
                {
                    Text = $"Новые {currentRowCount},{col + 1}",
                    BackgroundColor = currentRowCount % 2 == 1 ? Color.FromArgb("#f8f9fa") : Colors.White,
                    TextColor = Colors.Black,
                    Placeholder = $"Введите данные"
                };

                var border = new Border
                {
                    Content = entry,
                    Stroke = Color.FromArgb("#dee2e6"),
                    StrokeThickness = 1,
                    BackgroundColor = Colors.Transparent,
                    Padding = new Thickness(5)
                };

                MainTableGrid.Add(border, col, newRowIndex);
            }

            UpdateButtonsState();
        }
    }
}