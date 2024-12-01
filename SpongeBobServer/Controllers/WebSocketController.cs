using System.Net.WebSockets;
using System.Text;
using SpongeBobServer.Services;

namespace SpongeBobServer.Controllers
{
  public class WebSocketController
  {
    private readonly ConfigService _configService;

    public WebSocketController(ConfigService configService)
    {
      _configService = configService;
    }

    public async Task HandleWebSocket(HttpContext context)
    {
      if (context.WebSockets.IsWebSocketRequest)
      {
        using var webSocket = await context.WebSockets.AcceptWebSocketAsync();
        string clientIp = context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var config = _configService.LoadConfig();  // Load config before sending it to service
        config.Connected = true;
        config.ConnectedIp = clientIp;
        _configService.SaveConfig(config);  // Save updated config with connection info

        await WebSocketService.HandleWebSocket(webSocket, _configService, config); // Pass config explicitly
      }
      else
      {
        context.Response.StatusCode = 400; // Bad Request if it's not a WebSocket request
      }
    }
  }

  public static class WebSocketService
  {
    public static async Task HandleWebSocket(WebSocket webSocket, ConfigService configService, Models.Config config)
    {
      var buffer = new byte[1024];
      WebSocketReceiveResult result;
      string message = string.Empty;

      while (webSocket.State == WebSocketState.Open)
      {
        result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
        message = Encoding.UTF8.GetString(buffer, 0, result.Count);
        Console.WriteLine($"Received message: {message}");

        var parts = message.Trim().Split(":");

        if (parts.Length != 2)
        {
          Console.WriteLine("Invalid command");
          continue;
        }

        if (parts[0] == config.SecretCode)
        {
          var command = parts[1].Trim();
          switch (command.ToLower())
          {
            case "shutdown":
              CommandService.ShutdownPC();
              break;
            case "mouse_macro":
              CommandService.RunMouseMacro();
              break;
            case "screenshot":
              // Capture screenshot and send to mobile
              await CommandService.CaptureScreenshotAndSend(webSocket);
              break;
            default:
              Console.WriteLine("Unknown command");
              break;
          }

          string response = $"Command '{command}' executed";
          var responseBuffer = Encoding.UTF8.GetBytes(response);
          await webSocket.SendAsync(new ArraySegment<byte>(responseBuffer), WebSocketMessageType.Text, true, CancellationToken.None);
        }
        else
        {
          Console.WriteLine("Invalid secret code or command");
        }
      }

      // When WebSocket disconnects
      config.Connected = false;
      config.ConnectedIp = string.Empty;
      configService.SaveConfig(config); // Save updated config on disconnection
    }
  }
}
