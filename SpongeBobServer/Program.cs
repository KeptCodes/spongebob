
using SpongeBobServer.Services;
using SpongeBobServer.Controllers;
using System.Net;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
var ipAddress = GetLocalIPAddress();

// Create and load configuration service
var configService = new ConfigService("config.json");
var config = configService.LoadConfig();

// Set up controllers
var statusController = new StatusController(configService);
var secretCodeController = new SecretCodeController(configService);
var webSocketController = new WebSocketController(configService);

app.MapGet("/", statusController.GetStatusPage);
app.MapGet("/status", statusController.GetConnectionStatus);
app.MapGet("/save", secretCodeController.SaveSecretCode);

app.UseWebSockets();
app.Map("/ws", webSocketController.HandleWebSocket);

app.Run($"http://{ipAddress}:4200");

string GetLocalIPAddress()
{
    var host = Dns.GetHostEntry(Dns.GetHostName());
    var localIp = host.AddressList
        .FirstOrDefault(ip => ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork);
    return localIp?.ToString() ?? "127.0.0.1";
}
