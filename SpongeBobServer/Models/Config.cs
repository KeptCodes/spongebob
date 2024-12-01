namespace SpongeBobServer.Models
{
  public class Config
  {
    public string SecretCode { get; set; } = "12345";
    public bool Connected { get; set; } = false;
    public string ConnectedIp { get; set; } = string.Empty;
  }
}
