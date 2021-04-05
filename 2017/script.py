import meshio
import pandas as pd
import sys

points, cells, point_data, cell_data, field_data = meshio.read(sys.argv[1])
print (len (points))
coord = pd.DataFrame(points, columns=['X', 'Y', 'Z'])
coord.to_csv(sys.argv[2], sep='\t', encoding='utf-8', index=False)
