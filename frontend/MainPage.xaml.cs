using Microsoft.Maui.Controls;

namespace frontend
{
    public partial class MainPage : ContentPage
    {
        private Label welcomeLabel;
        private Button addDataButton;

        public MainPage()
        {
            CreateUI();
        }

        private void CreateUI()
        {
            welcomeLabel = new Label 
            { 
                Text = "Industrial Database App",
                FontSize = 32,
                HorizontalOptions = LayoutOptions.Center
            };

            addDataButton = new Button 
            { 
                Text = "Add New Data",
                BackgroundColor = Colors.Blue,
                TextColor = Colors.White,
                Padding = new Thickness(20, 10)
            };
            addDataButton.Clicked += OnAddDataClicked;

            Content = new ScrollView
            {
                Content = new VerticalStackLayout
                {
                    Spacing = 25,
                    Padding = 30,
                    Children = { welcomeLabel, addDataButton }
                }
            };
        }

        private async void OnAddDataClicked(object sender, System.EventArgs e)
        {
            welcomeLabel.Text = "Opening data form...";
            await Navigation.PushModalAsync(new AddDataPage());
        }
    }
}