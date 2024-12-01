using System;
using System.Diagnostics;
using System.IO;
using System.Net.WebSockets;
using Plugin.Screenshot;

namespace SpongeBobServer.Services
{
  public static class CommandService
  {
    public static void ShutdownPC()
    {
      Console.WriteLine("Shutting down PC...");
      // Uncomment to actually shutdown the PC
      Process.Start("shutdown", "/s /f /t 0");
    }

    public static void RunMouseMacro()
    {
      Console.WriteLine("Running Mouse Macro...");
      // Implement the mouse macro logic here
    }

    // Capture a screenshot using Xam.Plugin.Screenshot and send it to the WebSocket client
    public static async Task CaptureScreenshotAndSend(WebSocket webSocket)
    {
      try
      {
        Console.WriteLine("Capturing screenshot using Xam.Plugin.Screenshot...");

        // Capture the screenshot using Xam.Plugin.Screenshot
        string path = await CrossScreenshot.Current.CaptureAndSaveAsync();

        if (string.IsNullOrEmpty(path))
        {
          throw new Exception("Screenshot capture failed or returned an empty path.");
        }

        Console.WriteLine("Screenshot captured at path: " + path);

        // Read the screenshot from the file system
        byte[] screenshotData = await File.ReadAllBytesAsync(path);

        // Send the screenshot data over WebSocket
        await SendDataToWebSocket(webSocket, screenshotData);

      }
      catch (Exception ex)
      {
        Console.WriteLine($"Error capturing screenshot: {ex.Message}");
      }
    }


    // Helper method to send data over WebSocket
    private static async Task SendDataToWebSocket(WebSocket webSocket, byte[] data)
    {
      // Send the screenshot data as a binary message
      await webSocket.SendAsync(new ArraySegment<byte>(data), WebSocketMessageType.Binary, true, CancellationToken.None);
      Console.WriteLine("Screenshot sent to WebSocket client.");
    }
  }
}
