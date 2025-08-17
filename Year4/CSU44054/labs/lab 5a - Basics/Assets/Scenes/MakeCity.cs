using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class MakeCity : MonoBehaviour{
    public GameObject myBuilding;
    // Start is called before the first frame update
    void Start(){
        for (var i = -4; i<= 4; i++)
        {
            Vector3 newPosition = myBuilding.transform.position + new Vector3(i * 32.0f, 0, 0);
            //Instantiate([OBJECT TO COPY], [POSITION], [ROTATION]);
            Instantiate(myBuilding, newPosition, Quaternion.identity);
        }
    }

    // Update is called once per frame
    void Update(){
 
    }
}
