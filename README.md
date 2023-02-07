# Catchment generator
Tool for rapid prototyping of a hydraulic model that can be read and edited with SWMM.
The generator was created using feature analysis and surface runoff research from the literature. 
Fuzzy logic controller rules were developed using parameterized categories of soil, slope, 
and permeability. The catchment configuration procedure was simplified by mapping typical 
storage and Manning's coefficients. The use of fuzzy logic rules allows the system to be modified 
to adjust the categories to certain situations. The use of membership functions allows us to increase 
computation accuracy and customize the tool to diverse applications. Following alteration 
of the catchment in the SWMM GUI allows for accurate portrayal of the real condition of the catchment; 
no issues were encountered in altering the *inp file.

## Requirements
* Python 3

## Usage
To run the script, use the following command: 

```python3 pip install -r requirements``` 

```python3 main.py file_path``` where `file_path` is the path to the SWMM model file.

Then enter the catchment area and select the land use and land form categories.


## About
For the construction of the catchment generator, the type of land use was divided according to Table 1, 
the landform according to Table 2. 
The categories were determined on the basis of the data presented by (Dołęga, Rogala, 1973), given below in Table 3. 

### Table 1: Land use categories	
| Number  | Land Use                                     |
|---------|----------------------------------------------|
| 1       | marshes and lowlands                         |
| 2       | flats and plateaus                           |
| 3       | flats and plateaus in combination with hills |
| 4       | hills with gentle slopes                     |
| 5       | steeper hills and foothills                  |
| 6       | hills and outcrops of mountain ranges        |
| 7       | higher hills                                 |
| 8       | mountains                                    |
| 9       | highest mountains                            |



### Table 2 Landform categories	
| Number | Landform                    |
|--------|-----------------------------|
| 1      | medium conditions           |
| 2      | permeable areas             |
| 3      | permeable terrain on plains |
| 4      | hilly                       |
| 5      | mountains                   |
| 6      | bare rocky slopes           |
| 7      | urban                       |
| 8      | suburban                    |
| 9      | rural                       |
| 10     | forests                     |
| 11     | meadows                     |
| 12     | arable                      |
| 13     | marshes                     |

### Table 3. Runoff coefficients o according to Iszkowski

| Number | Topographic terrain definition  | Drainage coefficient ϕ |
|------|---------------------------------|----------------------|
| 1    | marshes and lowlands                         | 0.20                 |
| 2    | flats and plateaus                           | 0.25                 |
| 3    | flats and plateaus in combination with hills | 0.30                 |
| 4    | hills with gentle slopes                     | 0.35                 |
| 5    | steeper hills and foothills                  | 0.40                 |
| 6    | hills and outcrops of mountain ranges        | 0.45                 |
| 7    | higher hills                                 | 0.50                 |
| 8    | mountains                                    | 0.55                 |
| 9    | highest mountains                            | 0.60-0.70            |



##
Table 4 shows what and how feature values are generated. The "Value" column contains example data. 
### Table 4 SWMM catchment data.
| Parameter name      | Value      | Explanation                                                                                                                                                                                                                               |
| ------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name                | S1 [-]     | Catchment names (ID) are generated by adding a number.<br>                                                                                                                                                                                |
| Raingage            | 1 [-]      | When "raingage exists in the uploaded file, it will be assigned to the catchment area being built. If it does not exist, it will be added to the file along with the "timeseries" and assigned to the catchment area being generated.<br> |
| Outlet              | J1 [-]     | If there are receivers in the transferred file, the program will automatically assign it to the catchment area, if there are none, the name of the generated catchment area will be assigned.<br>                                         |
| Area                | 5 [ha]     | A parameter passed by the user.<br>                                                                                                                                                                                                       |
| Percent Imperv      | 25 [-]     | Parameter calculated as described above and assigned to the catchment area.<br>                                                                                                                                                           |
| Width               | 500 [m]    | The generated catchment areas are square in shape therefore the length of the side of the catchment area is assigned.<br>                                                                                                                 |
| Percent Slope       | 10 [-]     | Parameter calculated as described above and assigned to the catchment area.<br>                                                                                                                                                           |
| N-Imperv            | 0.15 [-]   | The value taken based on the linguistic variables passed to the fuzzy logic controller which were previously mapped with Manning coefficients.<br>                                                                                        |
| N-Perv              | 1 [-]      |The value taken based on the linguistic variables passed to the fuzzy logic controller which were previously mapped with Manning coefficients.
| Dstore-Imperv       | 1.27 [mm]  | The value taken based on the linguistic variables passed to the fuzzy logic controller which were previously mapped with typical storage values.<br>                                                                                      |
| Dstore-Perv         | 5.08 [mm]  |The value taken based on the linguistic variables passed to the fuzzy logic controller which were previously mapped with typical storage values.
| Percent Zero Imperv | 50 [-]     |The value taken based on the linguistic variables passed to the fuzzy logic controller which were previously mapped with typical storage values.
| RouteTo             | outlet [-] | Odpływ z obszarów imperv i perv spływa bezpośrednio do wylotu<br>                                                                                                                                                                         |
| Coordinate          | [-]        | Square-shaped catchments are generated, located so that one side is the edge of the contact.<br>                                                                                                                                          |