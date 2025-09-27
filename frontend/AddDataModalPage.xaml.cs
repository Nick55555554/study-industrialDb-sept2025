using Microsoft.Maui.Controls;
using Microsoft.Maui.Layouts;

namespace frontend
{
    public partial class AddDataPage : ContentPage
    {
        // Объявляем элементы управления как поля
        private Entry experimentNameEntry;
        private DatePicker experimentDatePicker;
        private Editor experimentDescriptionEditor;
        private Entry runNameEntry;
        private Picker runTypePicker;
        private Entry runParametersEntry;

        public AddDataPage()
        {
            // Создаем UI в коде вместо InitializeComponent()
            CreateUI();
            experimentDatePicker.Date = DateTime.Now;
        }

        private void CreateUI()
        {
            // Создаем элементы управления
            experimentNameEntry = new Entry { Placeholder = "Название эксперимента" };
            experimentDatePicker = new DatePicker();
            experimentDescriptionEditor = new Editor { 
                HeightRequest = 100, 
                Placeholder = "Описание эксперимента",
                AutoSize = EditorAutoSizeOption.TextChanges
            };
            runNameEntry = new Entry { Placeholder = "Название прогона" };
            runTypePicker = new Picker { 
                Title = "Выберите тип прогона",
                Items = { "Стандартный", "Калибровка", "Тестовый" }
            };
            runParametersEntry = new Entry { Placeholder = "Параметры прогона" };

            // Создаем кнопки
            var addButton = new Button 
            { 
                Text = "Добавить",
                BackgroundColor = Colors.Green,
                TextColor = Colors.White
            };
            addButton.Clicked += OnAddClicked;

            var clearButton = new Button 
            { 
                Text = "Очистить",
                BackgroundColor = Colors.Orange,
                TextColor = Colors.White
            };
            clearButton.Clicked += OnClearClicked;

            var closeButton = new Button 
            { 
                Text = "Закрыть",
                BackgroundColor = Colors.Red,
                TextColor = Colors.White
            };
            closeButton.Clicked += OnCloseClicked;

            // Создаем Grid для кнопок (правильный способ)
            var buttonsGrid = new Grid
            {
                ColumnDefinitions = 
                {
                    new ColumnDefinition { Width = GridLength.Star },
                    new ColumnDefinition { Width = GridLength.Star },
                    new ColumnDefinition { Width = GridLength.Star }
                },
                ColumnSpacing = 10
            };

            // Добавляем кнопки в Grid ПРАВИЛЬНЫМ способом
            buttonsGrid.Children.Add(addButton);
            Grid.SetColumn(addButton, 0);

            buttonsGrid.Children.Add(clearButton);
            Grid.SetColumn(clearButton, 1);

            buttonsGrid.Children.Add(closeButton);
            Grid.SetColumn(closeButton, 2);

            // Создаем layout
            Content = new ScrollView
            {
                Content = new VerticalStackLayout
                {
                    Spacing = 15,
                    Padding = 20,
                    Children = 
                    {
                        new Label { 
                            Text = "Добавление данных", 
                            FontSize = 24, 
                            FontAttributes = FontAttributes.Bold, 
                            HorizontalOptions = LayoutOptions.Center 
                        },
                        
                        new Label { 
                            Text = "Название эксперимента:", 
                            FontSize = 16, 
                            FontAttributes = FontAttributes.Bold 
                        },
                        experimentNameEntry,
                        
                        new Label { 
                            Text = "Дата эксперимента:", 
                            FontSize = 16, 
                            FontAttributes = FontAttributes.Bold 
                        },
                        experimentDatePicker,
                        
                        new Label { 
                            Text = "Описание:", 
                            FontSize = 16, 
                            FontAttributes = FontAttributes.Bold 
                        },
                        experimentDescriptionEditor,
                        
                        new Label { 
                            Text = "Название прогона:", 
                            FontSize = 16, 
                            FontAttributes = FontAttributes.Bold 
                        },
                        runNameEntry,
                        
                        new Label { 
                            Text = "Тип прогона:", 
                            FontSize = 16, 
                            FontAttributes = FontAttributes.Bold 
                        },
                        runTypePicker,
                        
                        new Label { 
                            Text = "Параметры:", 
                            FontSize = 16, 
                            FontAttributes = FontAttributes.Bold 
                        },
                        runParametersEntry,
                        
                        buttonsGrid
                    }
                }
            };
        }

        private async void OnAddClicked(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(experimentNameEntry.Text))
            {
                await DisplayAlert("Ошибка", "Введите название эксперимента", "OK");
                return;
            }
            
            // Собираем данные
            var experimentData = new
            {
                Name = experimentNameEntry.Text,
                Date = experimentDatePicker.Date,
                Description = experimentDescriptionEditor.Text,
                RunName = runNameEntry.Text,
                RunType = runTypePicker.SelectedItem?.ToString(),
                Parameters = runParametersEntry.Text
            };
            
            await DisplayAlert("Успех", "Данные добавлены в базу данных", "OK");
            await Navigation.PopModalAsync();
        }

        private void OnClearClicked(object sender, EventArgs e)
        {
            experimentNameEntry.Text = string.Empty;
            experimentDatePicker.Date = DateTime.Now;
            experimentDescriptionEditor.Text = string.Empty;
            runNameEntry.Text = string.Empty;
            runTypePicker.SelectedIndex = -1;
            runParametersEntry.Text = string.Empty;
        }

        private async void OnCloseClicked(object sender, EventArgs e)
        {
            bool result = await DisplayAlert("Подтверждение", 
                "Закрыть форму без сохранения?", "Да", "Нет");
            
            if (result)
            {
                await Navigation.PopModalAsync();
            }
        }
    }
}