using Microsoft.AspNetCore.Http;
using SpongeBobServer.Services;

namespace SpongeBobServer.Controllers
{
  public class StatusController
  {
    private readonly ConfigService _configService;

    public StatusController(ConfigService configService)
    {
      _configService = configService;
    }

    public async Task GetStatusPage(HttpContext context)
    {
      var html = @"
            <html>
                <head>
                    <title>Spongebob Server Status</title>
                    <script>
                        function checkConnection() {
                            fetch('/status')
                                .then(response => response.json())
                                .then(data => {
                                    if (data.connected) {
                                        document.getElementById('status').innerText = 'Connected to Mobile: ' + data.ip;
                                        document.getElementById('status').style.color = 'green';
                                    } else {
                                        document.getElementById('status').innerText = 'Not Connected';
                                        document.getElementById('status').style.color = 'red';
                                    }
                                });
                        }
                        setInterval(checkConnection, 2000);
                    </script>
                </head>
                <body>
                    <h1>WebSocket Server Status</h1>
                    <p id='status'>Checking...</p>
                    <label for='secretCode'>Enter Secret Code:</label>
                    <input type='text' id='secretCode' />
                    <button onclick='sendSecretCode()'>Save</button>

                    <script>
                        function sendSecretCode() {
                            var code = document.getElementById('secretCode').value;
                            fetch('/save?code=' + code)
                                .then(response => response.json())
                                .then(data => alert(data.message));
                        }
                    </script>
                </body>
            </html>";

      context.Response.ContentType = "text/html";
      await context.Response.WriteAsync(html);
    }

    public IResult GetConnectionStatus()
    {
      var config = _configService.LoadConfig();
      return Results.Json(new { connected = config.Connected, ip = config.ConnectedIp });
    }
  }
}
