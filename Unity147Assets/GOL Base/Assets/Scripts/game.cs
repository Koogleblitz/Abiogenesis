using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class game : MonoBehaviour
{

    private static int SCREEN_WIDTH = 64; //1024
    private static int SCREEN_HEIGHT = 48; //768

    public float speed = 0.1f; //control speed of game
    private float timer = 0;    //init timer to zero - to be incremented

    cell[,] grid = new cell[SCREEN_WIDTH, SCREEN_HEIGHT];

    // Start is called before the first frame update
    void Start()
    {
        PlaceCells(); //spawn cells
    }

    // Update is called once per frame
    void Update()
    {

        if (timer >= speed)
        {
            timer = 0f;
            CountNeighbors(); //iterate grid and count neighbors
            PopulationControl(); //kill or revive cells based on 3 rules
        }
        else
        {
            timer += Time.deltaTime; // increment by time passed since last frame
        }
    }

    void PlaceCells()
    { //iterate entire screen
        for(int y = 0; y<SCREEN_HEIGHT; y++)
        {
            for (int x = 0; x<SCREEN_WIDTH; x++)
            {
                cell c = Instantiate(Resources.Load("prefabs/cell", typeof(cell)), new Vector2(x, y), Quaternion.identity) as cell;
                grid[x, y] = c;
                grid[x, y].SetAlive(randomAliveCell());
            }
        }
    }

    void CountNeighbors()
    {
        for(int y = 0; y<SCREEN_HEIGHT; y++)
        {
            for(int x = 0; x<SCREEN_WIDTH; x++)
            {
                int neighbor_count = 0;

                // ~~ north neighbor check
                if(y+1 < SCREEN_HEIGHT) //boundary checking for max height
                {
                    if(grid[x,y+1].isAlive)
                    {
                        neighbor_count++;
                    }
                }
                // ~~ east neighbor check
                if (x + 1 < SCREEN_WIDTH) //boundary checking for max width - east side
                {
                    if (grid[x+1, y].isAlive)
                    {
                        neighbor_count++;
                    }
                }
                //south
                if(y-1 >= 0)
                {
                    if(grid[x,y-1].isAlive)
                    {
                        neighbor_count++;
                    }
                }
                //west
                if(x-1 >= 0)
                {
                    if(grid[x-1,y].isAlive)
                    {
                        neighbor_count++;
                    }
                }
                //Northeast
                if(x+1 < SCREEN_WIDTH && y+1 < SCREEN_HEIGHT)
                {
                    if(grid[x+1,y+1].isAlive)
                    {
                        neighbor_count++;
                    }
                }
                //NW
                if (x - 1 >= 0 && y + 1 < SCREEN_HEIGHT)
                {
                    if (grid[x - 1, y + 1].isAlive)
                    {
                        neighbor_count++;
                    }
                }
                //se
                if (x + 1 < SCREEN_WIDTH && y - 1 >= 0)
                {
                    if (grid[x + 1, y - 1].isAlive)
                    {
                        neighbor_count++;
                    }
                }
                //sw
                if (x - 1 >=0 && y - 1 >= 0)
                {
                    if (grid[x - 1, y - 1].isAlive)
                    {
                        neighbor_count++;
                    }
                }
                
                grid[x,y].neighbor_count = neighbor_count; //number of neighbors for each cell
            }
        }
    }

    void PopulationControl()
    {
        for(int y = 0; y < SCREEN_HEIGHT; y++)
        {
            for(int x = 0; x < SCREEN_WIDTH; x++)
            {
                //conway gol rules:
                //1 - any live cell with 2 or 3 neighbors survives
                //2 - any dead cell with 3 live neighbors becomes a live cell
                //3 - all other live cells die in the next generation and all other dead cells stay dead

                if(grid[x,y].isAlive)
                {
                    //cell is alive
                    //rule 1 - any live cell with 2 or 3 neighbors survives
                    if (grid[x,y].neighbor_count != 2 && grid[x, y].neighbor_count != 3)
                    {
                        grid[x,y].SetAlive(false); //kill the cell 
                    }
                }
                else
                {
                    //already dead
                    //2 - any dead cell with 3 live neighbors becomes a live cell
                    if (grid[x,y].neighbor_count == 3)
                    {
                        grid[x, y].SetAlive(true);
                    }
                }
            }
        }
    }

    bool randomAliveCell()
    {
        int rand = UnityEngine.Random.Range(0,100);

        if(rand > 75)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}
