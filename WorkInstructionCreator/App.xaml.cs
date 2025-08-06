using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System.Windows;
using WorkInstructionCreator.Services;
using WorkInstructionCreator.ViewModels;

namespace WorkInstructionCreator;

public partial class App : Application
{
    private IHost? _host;

    protected override async void OnStartup(StartupEventArgs e)
    {
        _host = Host.CreateDefaultBuilder()
            .ConfigureServices((context, services) =>
            {
                // Services
                services.AddSingleton<ITemplateService, TemplateService>();
                services.AddSingleton<IFlowchartService, FlowchartService>();
                services.AddSingleton<IDocumentExportService, DocumentExportService>();
                services.AddSingleton<IChatbotService, ChatbotService>();
                services.AddSingleton<IContentLibraryService, ContentLibraryService>();

                // ViewModels
                services.AddTransient<MainWindowViewModel>();
                services.AddTransient<EditorViewModel>();
                services.AddTransient<TemplateSelectionViewModel>();
                services.AddTransient<FlowchartViewModel>();
                services.AddTransient<ContentLibraryViewModel>();
            })
            .Build();

        await _host.StartAsync();

        base.OnStartup(e);
    }

    protected override async void OnExit(ExitEventArgs e)
    {
        if (_host != null)
        {
            await _host.StopAsync();
            _host.Dispose();
        }

        base.OnExit(e);
    }

    public static T GetService<T>() where T : class
    {
        return ((App)Current)._host?.Services.GetRequiredService<T>() 
               ?? throw new InvalidOperationException("Service not available");
    }
}