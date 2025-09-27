using Microsoft.Maui.LifecycleEvents;
using Microsoft.Windows.AppNotifications;

namespace IndustrialDbWorkingFrontend
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();
            builder
                .UseMauiApp<App>()
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                })
                .ConfigureLifecycleEvents(events =>
                {
#if WINDOWS
                    events.AddWindows(windows => windows
                        .OnLaunch((app, args) =>
                        {
                            // Инициализация функций Windows 11
                            InitializeWindows11Features();
                        })
                        .OnClosed((app, args) =>
                        {
                            // Очистка ресурсов
                        }));
#endif
                });

#if DEBUG
            builder.Logging.AddDebug();
#endif

            return builder.Build();
        }

#if WINDOWS
        private static void InitializeWindows11Features()
        {
            try
            {
                // Инициализация уведомлений Windows 11
                var notificationManager = Microsoft.Windows.AppNotifications.AppNotificationManager.Default;
                
                // Можно добавить специфичные функции Windows 11 здесь
            }
            catch (Exception ex)
            {
                // Фолбэк для Windows 10
                System.Diagnostics.Debug.WriteLine($"Windows 11 features not available: {ex.Message}");
            }
        }
#endif
    }
}