import pandas as pd
import os.path
import math
from qgis.PyQt.QtCore import QVariant

from qgis.core import *

### PUT VALUES HERE ###

'''
  suggested project structure:
    .
    ├── aoi
    ├── intersects
    │   ├── coastCR
    │   └── coastSat
    ├── positions
    ├── pyscripts
    ├── rates
    └── transects

  ensure that all these folders are present
'''

intersects_filename = 'intersects.csv'  # csv
transects_filename = 'transects_landward_baseline0.shp'   # shp
### END ###

class MetricsCalculator:
  def __init__(self) -> None:
    self.intersects: pd.DataFrame 
    self.transects: QgsVectorLayer
    self.homePath: str = QgsProject.instance().homePath()
    self.output_dir: str = QgsProject.instance().homePath() + '/rates/'

  def loadLayers(self, intersects_filename: str, transects_filename: str):
    '''
      loads necessary files for computation 
      intersects_filename: points to a csv file of all intersects with transects
      transects_filename: points to a shp of all transects 

      assumed locations:
        intersects is assumed to be in intersects folder
        transects is assumed to be in transects folder
    '''
    intersects_filePath = self.homePath+'/intersects/'+intersects_filename
    transects_filePath = self.homePath+'/transects/'+transects_filename

    # check if file exists
    if os.path.isfile(intersects_filePath) == False:
      print("warning! {fn} does not exist".format(fn=intersects_filePath))
      exit 
    if os.path.isfile(transects_filePath) == False:
      print("warning! {fn} does not exist".format(fn=transects_filePath))
      exit

    # note this later
    # self.intersects = pd.read_csv(intersects_filePath, index_col=0)
    self.intersects = pd.read_csv(intersects_filePath)
    self.transects = QgsVectorLayer(transects_filePath)

  def calcNSM(self, row: pd.Series):
    '''
      youngest_position_intersect - oldest_position_intersect 
      negative if youngest position is closer to transect origin than oldest position
      which signifies the occurence of regression
    '''
    transectName = row['Normal']
    youngest_position = self.intersects.loc[self.intersects['dates'] == max(self.intersects['dates'])][transectName].iloc[0]
    oldest_position = self.intersects.loc[self.intersects['dates'] == min(self.intersects['dates'])][transectName].iloc[0]

    return youngest_position - oldest_position

  def calcSCE(self, row: pd.Series):
    transectName = row['Normal']
    return max(self.intersects[transectName]) - min(self.intersects[transectName])

  def calcLRR(self, row: pd.Series):
    transectName = row['Normal']

    intersect_table = pd.DataFrame()
    intersect_table['x'] = self.intersects['dates']
    intersect_table['y'] = self.intersects[transectName]
    intersect_table['xy'] = intersect_table['x'] * intersect_table['y'] 
    intersect_table['x_squared'] = intersect_table['x'] ** 2

    # set number of rows (intersections as n)
    n_intersects = intersect_table.shape[0]

    sumX = intersect_table['x'].sum()
    sumY = intersect_table['y'].sum()
    sumX_squared = intersect_table['x_squared'].sum()
    sumXY = intersect_table['xy'].sum()
    squared_sumX = sumX**2

    m = ((n_intersects*sumXY)-(sumX * sumY))/((n_intersects*sumX_squared) - (squared_sumX))
    return m # slope

  def calcWLRR(self):
    pass

  def toShp(self, rates: pd.DataFrame):
    '''
      turns shp file into a normal rates shape file.
      give geometry
    '''

    fields = QgsFields()
    fields.append(QgsField(rates.columns[0], QVariant.String))
    for col in rates.columns[1:]:
      fields.append(QgsField(col, QVariant.Double))

    writer = QgsVectorFileWriter(
      self.output_dir + 'normal_rates.shp',
      'UTF-8', 
      fields,
      QgsWkbTypes.LineString, 
      srs=QgsProject.instance().crs(),
      driverName="ESRI Shapefile"
    )

    transect_rates = []
    for row in rates.iterrows():
      transect_rates.append(row[1].tolist())

    # get geometries of transects
    print(self.transects)
    transect_geoms = [transect.geometry() for transect in self.transects.getFeatures()]

    # get max geometry
    # for visualizing different rates
    # ...

    for transect_attrs in zip(transect_geoms, transect_rates):
      geom = transect_attrs[0]
      attrs = transect_attrs[1]
      fet = QgsFeature()

      fet.setGeometry(geom)
      fet.setAttributes(attrs)

      writer.addFeature(fet)
    
    del writer

  def toCSV(self, rates: pd.DataFrame):
    output = self.output_dir + '/normal_rates.csv' 
    rates.to_csv(output)

  def summarize(self, rates: pd.DataFrame):
    summary = rates.describe()
    output = self.output_dir + '/summary.csv' 
    summary.to_csv(output)

  def setupTransects(self):
    pass

  def setupIntersects(self) -> pd.DataFrame:
    transect_rates = pd.DataFrame()
    
    print(self.intersects.columns)

    # prepreocess intersects
    self.intersects['dates'] = pd.to_datetime(self.intersects['dates'])
    oldest_date = min(self.intersects['dates']).to_pydatetime()
    self.intersects['dates'] = [  (date_.to_pydatetime() - oldest_date).days/365 for date_ in self.intersects['dates'] ]

    transect_rates['Normal'] = self.intersects.columns[1:] 
    transect_rates['NSM'] = [math.nan for i in transect_rates['Normal']]
    transect_rates['SCE'] = [math.nan for i in transect_rates['Normal']]
    transect_rates['LRR'] = [math.nan for i in transect_rates['Normal']]
    transect_rates['WLRR'] = [math.nan for i in transect_rates['Normal']]

    return transect_rates
  
  def run(self):
    # set_up intersects dataframe 
    self.transect_rates = self.setupIntersects()

    self.transect_rates['NSM'] = self.transect_rates.apply(self.calcNSM, axis=1)
    self.transect_rates['SCE'] = self.transect_rates.apply(self.calcSCE, axis=1)
    self.transect_rates['LRR'] = self.transect_rates.apply(self.calcLRR, axis=1)
    # self.transect_rates['WLRR'] = self.transect_rates.apply(self.calcWLRR, axis=1)

    self.toShp(self.transect_rates)
    self.toCSV(self.transect_rates)
    self.summarize(self.transect_rates)

    print('calculations done')

mc = MetricsCalculator()
mc.loadLayers(intersects_filename, transects_filename)
mc.run()