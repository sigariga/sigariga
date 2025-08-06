using System.Windows;
using WorkInstructionCreator.ViewModels;

namespace WorkInstructionCreator.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        DataContext = App.GetService<MainWindowViewModel>();
    }
}