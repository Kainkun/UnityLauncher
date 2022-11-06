//v1.1
using System.IO;
using System.Threading.Tasks;
using UnityEditor;
using UnityEngine;

namespace Editor.UnityLauncher
{
    public class MenuItems : MonoBehaviour
    {
        [MenuItem("Unity Launcher/Screenshot Project Icon")]
        public static async void Screenshot()
        {
            string projectPath = Path.GetDirectoryName(Application.dataPath);
            if (projectPath == null)
                return;

            string iconFilePath = Path.Combine(projectPath, "icon.png");

            File.Delete(iconFilePath);
            ScreenCapture.CaptureScreenshot(iconFilePath);
            while (!File.Exists(iconFilePath))
                await Task.Yield();

            //Crop
            byte[] fileData = File.ReadAllBytes(iconFilePath);
            Texture2D texture = new Texture2D(2, 2);
            texture.LoadImage(fileData);
            int minSize;
            if (texture.width < texture.height)
                minSize = texture.width;
            else
                minSize = texture.height;
            Color[] c = texture.GetPixels((texture.width / 2) - (minSize / 2), (texture.height / 2) - (minSize / 2), minSize, minSize);
            Texture2D icon = new Texture2D(minSize, minSize, TextureFormat.ARGB32, false);
            icon.SetPixels(c);
            icon.Apply();
            
            TextureScale.Scale(icon, 300, 300);
            
            byte[] byteArray = icon.EncodeToPNG();
            System.IO.File.WriteAllBytes(iconFilePath, byteArray);

            //Display Icon
            System.Diagnostics.Process.Start(iconFilePath);
        }

        [MenuItem("Unity Launcher/Set Project Description")]
        public static void SetProjectDescription()
        {
            string projectPath = Path.GetDirectoryName(Application.dataPath);
            if (projectPath == null)
                return;

            string descriptionFilePath = Path.Combine(projectPath, "description.txt");

            if (!File.Exists(descriptionFilePath))
                File.Create(descriptionFilePath).Close();

            System.Diagnostics.Process.Start(descriptionFilePath);
        }
    }
}