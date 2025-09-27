using Microsoft.Maui.Controls;

namespace frontend
{
    public partial class App : Application
    {
        public App()
        {
            // Убрали устаревшее свойство MainPage
        }

        protected override Window CreateWindow(IActivationState activationState)
        {
            // Современный подход - создаем Window напрямую
            return new Window(new NavigationPage(new MainPage()))
            {
                Title = "Industrial Database App",
                Width = 1200,
                Height = 800
            };
        }
    }
}