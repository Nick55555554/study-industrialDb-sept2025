using Microsoft.Maui.Controls;
using Microsoft.Maui.Layouts;

namespace frontend
{
    public partial class ShowDataPage : ContentPage
    {
        public ShowDataPage()
        {
            CreateUI();
        }

        private void CreateUI()
        {
            var backButton = new ToolbarItem { Text = "Назад" };
            backButton.Clicked += OnBackClicked;

            var refreshButton = new ToolbarItem { Text = "Обновить" };
            refreshButton.Clicked += OnRefreshClicked;

            ToolbarItems.Add(backButton);
            ToolbarItems.Add(refreshButton);

            var titleLabel = new Label
            {
                Text = "Сводная таблица EXPERIMENTS/RUNS",
                FontSize = 20,
                FontAttributes = FontAttributes.Bold,
                HorizontalOptions = LayoutOptions.Center
            };

            // Заголовок таблицы
            var headerGrid = CreateHeaderGrid();

            // Данные таблицы
            var dataContainer = new VerticalStackLayout { Spacing = 5 };

            // Пример данных
            AddDataRow(dataContainer, "Тест производительности", "15.12.2024", "Запуск #1", "Производственный", "Завершен", Colors.Green);
            AddDataRow(dataContainer, "Анализ данных", "16.12.2024", "Запуск #2", "Экспериментальный", "В процессе", Colors.Orange);

            // Статистика
            var statsLayout = new HorizontalStackLayout { Spacing = 20 };
            statsLayout.Children.Add(new Label { Text = "Всего записей: 2", FontAttributes = FontAttributes.Bold });
            statsLayout.Children.Add(new Label { Text = "Завершено: 1", TextColor = Colors.Green, FontAttributes = FontAttributes.Bold });
            statsLayout.Children.Add(new Label { Text = "В процессе: 1", TextColor = Colors.Orange, FontAttributes = FontAttributes.Bold });

            var statsBorder = new Border
            {
                BackgroundColor = Color.FromArgb("#E8F4FD"),
                Padding = 15,
                Stroke = Colors.Transparent,
                Content = statsLayout
            };

            Content = new ScrollView
            {
                Content = new VerticalStackLayout
                {
                    Spacing = 15,
                    Padding = 20,
                    Children = { titleLabel, headerGrid, dataContainer, statsBorder }
                }
            };
        }

        private Grid CreateHeaderGrid()
        {
            var grid = new Grid
            {
                ColumnDefinitions =
                {
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) },
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) },
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) },
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) },
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) }
                },
                BackgroundColor = Color.FromArgb("#343A40"),
                Padding = 10
            };

            // Правильное использование Grid.SetColumn
            var label1 = new Label { Text = "Эксперимент", TextColor = Colors.White, FontAttributes = FontAttributes.Bold };
            grid.Children.Add(label1);
            Microsoft.Maui.Controls.Grid.SetColumn(label1, 0); // Явное указание класса

            var label2 = new Label { Text = "Дата", TextColor = Colors.White, FontAttributes = FontAttributes.Bold };
            grid.Children.Add(label2);
            Microsoft.Maui.Controls.Grid.SetColumn(label2, 1);

            var label3 = new Label { Text = "Запуск", TextColor = Colors.White, FontAttributes = FontAttributes.Bold };
            grid.Children.Add(label3);
            Microsoft.Maui.Controls.Grid.SetColumn(label3, 2);

            var label4 = new Label { Text = "Тип", TextColor = Colors.White, FontAttributes = FontAttributes.Bold };
            grid.Children.Add(label4);
            Microsoft.Maui.Controls.Grid.SetColumn(label4, 3);

            var label5 = new Label { Text = "Статус", TextColor = Colors.White, FontAttributes = FontAttributes.Bold };
            grid.Children.Add(label5);
            Microsoft.Maui.Controls.Grid.SetColumn(label5, 4);

            return grid;
        }

        private void AddDataRow(Layout parent, string experiment, string date, string run, string type, string status, Color statusColor)
        {
            var rowGrid = new Grid
            {
                ColumnDefinitions =
                {
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) },
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) },
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) },
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) },
                    new ColumnDefinition { Width = new GridLength(2, GridUnitType.Star) }
                },
                BackgroundColor = parent.Children.Count % 2 == 0 ? Color.FromArgb("#F8F9FA") : Colors.White,
                Padding = 10,
                HeightRequest = 40
            };

            // Правильное добавление элементов в Grid
            var expLabel = new Label { Text = experiment, FontSize = 12 };
            rowGrid.Children.Add(expLabel);
            Microsoft.Maui.Controls.Grid.SetColumn(expLabel, 0);

            var dateLabel = new Label { Text = date, FontSize = 12 };
            rowGrid.Children.Add(dateLabel);
            Microsoft.Maui.Controls.Grid.SetColumn(dateLabel, 1);

            var runLabel = new Label { Text = run, FontSize = 12 };
            rowGrid.Children.Add(runLabel);
            Microsoft.Maui.Controls.Grid.SetColumn(runLabel, 2);

            var typeLabel = new Label { Text = type, FontSize = 12 };
            rowGrid.Children.Add(typeLabel);
            Microsoft.Maui.Controls.Grid.SetColumn(typeLabel, 3);

            var statusLabel = new Label { Text = status, TextColor = statusColor, FontSize = 12 };
            rowGrid.Children.Add(statusLabel);
            Microsoft.Maui.Controls.Grid.SetColumn(statusLabel, 4);

            parent.Children.Add(rowGrid);
        }

        private async void OnRefreshClicked(object sender, EventArgs e)
        {
            await DisplayAlert("Обновление", "Данные обновлены", "OK");
        }

        private async void OnBackClicked(object sender, EventArgs e)
        {
            await Navigation.PopAsync();
        }
    }
}