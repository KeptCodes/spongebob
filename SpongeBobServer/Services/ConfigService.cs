using Newtonsoft.Json;
using SpongeBobServer.Models;
using System.IO;

namespace SpongeBobServer.Services
{
  public class ConfigService
  {
    private readonly string _configFilePath;

    public ConfigService(string configFilePath)
    {
      _configFilePath = configFilePath;
    }

    public Config LoadConfig()
    {
      if (File.Exists(_configFilePath))
      {
        var json = File.ReadAllText(_configFilePath);
        return JsonConvert.DeserializeObject<Config>(json) ?? new Config();
      }
      return new Config();
    }

    public void SaveConfig(Config config)
    {
      var json = JsonConvert.SerializeObject(config, Formatting.Indented);
      File.WriteAllText(_configFilePath, json);
    }
  }
}
