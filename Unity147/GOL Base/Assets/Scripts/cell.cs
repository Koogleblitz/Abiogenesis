using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cell : MonoBehaviour
{
    public bool isAlive = false;
    public int neighbor_count = 0;

    public void SetAlive(bool alive)
    {
        isAlive = alive;

        if(alive) //cell alive
        {
            GetComponent<SpriteRenderer>().enabled = true;
        }
        else // cell is dead 
        {
            GetComponent<SpriteRenderer>().enabled = false;
        }
    }
}
