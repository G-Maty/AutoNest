using UnityEngine;
using UnityEditor;

/// <summary>
/// Unity Editor用のサンプルスクリプト
/// AutoNestで自動生成されました
/// </summary>
public class EditorScript : EditorWindow
{
    [MenuItem("Tools/Custom Editor Tool")]
    public static void ShowWindow()
    {
        GetWindow<EditorScript>("Custom Tool");
    }

    private void OnGUI()
    {
        GUILayout.Label("Custom Editor Tool", EditorStyles.boldLabel);
        
        if (GUILayout.Button("実行"))
        {
            Debug.Log("カスタムツールが実行されました");
        }
        
        if (GUILayout.Button("リセット"))
        {
            Debug.Log("リセットされました");
        }
    }
}
