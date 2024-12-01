using Microsoft.AspNetCore.Http;
using SpongeBobServer.Services;

namespace SpongeBobServer.Controllers
{
  public class SecretCodeController
  {
    private readonly ConfigService _configService;

    public SecretCodeController(ConfigService configService)
    {
      _configService = configService;
    }

    public IResult SaveSecretCode(string code)
    {
      var config = _configService.LoadConfig();
      config.SecretCode = code;
      _configService.SaveConfig(config);
      return Results.Json(new { message = "Code Saved!" });
    }
  }
}
