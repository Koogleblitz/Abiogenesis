using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class ConwaysGameOfLife : MonoBehaviour
{
    public Texture input;

    public int width = 2048;
    public int height = 2048;

    public ComputeShader compute;
    public RenderTexture result;
    public Material material;

    //timer implemeted for display purposes
    public float speed = 0.25f; //control speed of game
    private float timer = 0;    //init timer to zero - to be incremented
    public int kernel_access_count = 0;//count the number of times we access the kernel

    // Start is called before the first frame update
    void Start()
    {
        result = new RenderTexture(width, height, 24);
        result.enableRandomWrite = true;
        result.Create();
    }

    // Update is called once per frame
    void Update()
    {
        if (height < 1 || width < 1)
        {
            return;
        }

        // if (timer >= speed) //timer reached checkpoint - update
        // {
        // timer = 0f; //re-initialze on success

        kernel_access_count++;
        Debug.Log("kernel access: " + kernel_access_count);

        int kernel = compute.FindKernel("GameOfLife");


        compute.SetTexture(kernel, "Input", input); //input - image to be proccessed by kernel
        compute.SetFloat("Width", width); // enable width input
        compute.SetFloat("Height", height); //enable height input

        result = new RenderTexture(width, height, 24);
        result.wrapMode = TextureWrapMode.Repeat;   //loops after finished animation
        result.enableRandomWrite = true;
        result.filterMode = FilterMode.Point;
        result.Create();

        compute.SetTexture(kernel, "Result", result);
        compute.Dispatch(kernel, width / 8, height / 8, 1);

        input = result;
        material.mainTexture = input; //set material

        //  }
        // else
        // {
        //timer += ((Time.deltaTime)*25); // increment by time passed since last frame
        // }

    }
}
