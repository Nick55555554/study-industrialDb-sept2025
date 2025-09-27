namespace frontend
{
    public partial class AppShell : Shell
    {
        public AppShell()
        {
            // Уберите InitializeComponent() и создайте Shell в коде
            var mainPage = new ShellContent
            {
                Title = "Home",
                ContentTemplate = new DataTemplate(() => new MainPage()),
                Route = "MainPage"
            };

            Items.Add(mainPage);
            FlyoutBehavior = FlyoutBehavior.Disabled;
        }
    }
}