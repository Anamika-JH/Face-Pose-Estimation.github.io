using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using UnityEngine;
using System.Net;
using System.Text;
using System;

public class HeadPoseReceiver : MonoBehaviour
{
byte[] data;
UdpClient listener;
IPEndPoint remoteEndPoint;
string receivedTranslation;

// Averaging parameters
int frameCount = 5;
Vector3[] poseBuffer;
int currentFrame = 0;
float scale = 0.01f; // Adjust scale as needed
float scale1 = 0.01f;
float minXPosition = -2.6f;
float maxXPosition = 2.6f;
float maxYPosition = 2.2f;
float minYPosition = -0.4f;
void Start()
{
listener = new UdpClient(54000);
remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
data = new byte[1024];
receivedTranslation = "0;0;0"; // Default translation

poseBuffer = new Vector3[frameCount];

StartCoroutine(ReceiveData());
}

IEnumerator ReceiveData()
{
while (true)
{
data = listener.Receive(ref remoteEndPoint);
receivedTranslation = Encoding.ASCII.GetString(data, 0, data.Length);
yield return null;
}
}

void Update()
{
// Parse received translation
string[] translationValues = receivedTranslation.Split(';');
float translationX = float.Parse(translationValues[0]) * scale;
float translationY = float.Parse(translationValues[1]) * scale;
float translationZ = (float.Parse(translationValues[2]) + 65 ) * scale1;

// Calculate displacement based on translation values
Vector3 displacement = new Vector3(translationX, translationY, translationZ);

// Add the current displacement to the buffer
poseBuffer[currentFrame % frameCount] = displacement;

// Increment the frame counter
currentFrame++;

// Check if we have enough frames in the buffer
if (currentFrame >= frameCount)
{
// Calculate the average displacement from the buffer
Vector3 averagedDisplacement = AverageVector(poseBuffer);

// Update Main Camera's position based on the averaged displacement
Vector3 newPosition = Camera.main.transform.position + new Vector3(averagedDisplacement.x, averagedDisplacement.y, averagedDisplacement.z);
// Clamp the x-position an y-position
newPosition.x = Mathf.Clamp(newPosition.x, minXPosition, maxXPosition);
newPosition.y = Mathf.Clamp(newPosition.y, minYPosition, maxYPosition);
newPosition.z = Mathf.Clamp(newPosition.z, -12, -6);
Camera.main.transform.position = newPosition;
}
}

Vector3 AverageVector(Vector3[] vectors)
{
if (vectors.Length == 0)
{
return Vector3.zero;
}

Vector3 sum = Vector3.zero;
foreach (Vector3 v in vectors)
{
sum += v;
}

return sum / vectors.Length;
}

private void OnApplicationQuit()
{
listener.Close();
}
}