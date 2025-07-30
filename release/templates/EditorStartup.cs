using UnityEditor;
using UnityEngine;

[InitializeOnLoad]
public class EditorStartup
{
    static EditorStartup()
    {
        Debug.Log("🛠️ Unity Editor 起動検知！");

        // 起動時に実行したい処理を書く
    }
}