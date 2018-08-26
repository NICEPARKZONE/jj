import sys
sys.path.extend(['/home/pedrolisboa/Workspace/lps/SonarAnalysis/'])

from Functions.TrainFunctions import ConvolutionTrainFunction
from Functions.ConvolutionalNeuralNetworks import KerasModel
from Functions.TrainParameters import TrnParamsConvolutional
import os
from Functions.CrossValidation import NestedCV, SonarRunsCV
from Functions.NpUtils.DataTransformation import lofar2image, SonarRunsInfo
from Functions.SystemIO import exists, mkdir

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from sklearn.externals import joblib

# Database caracteristics
datapath = os.getenv('OUTPUTDATAPATH')

audiodatapath = os.getenv('INPUTDATAPATH')
database = '4classes'
n_pts_fft = 1024
decimation_rate = 3
spectrum_bins_left = 400

# Check if LofarData has created...
if not os.path.exists('%s/%s/lofar_data_file_fft_%i_decimation_%i_spectrum_left_%i.jbl' %
                      (datapath, database, n_pts_fft, decimation_rate, spectrum_bins_left)):
    print 'No Files in %s/%s\n' % (datapath, database)
else:
    # Read lofar data
    dataset = joblib.load('%s/%s/lofar_data_file_fft_%i_decimation_%i_spectrum_left_%i.jbl' %
                                             (datapath, database, n_pts_fft, decimation_rate, spectrum_bins_left))

data = dataset[0]
trgt = dataset[1]
class_labels = dataset[2]

dataset = [data,trgt,class_labels]

ncv = NestedCV(5, 10, datapath, audiodatapath)
if ncv.exists():
    ncv.loadCVs()
else:
    ncv.createCVs(data, trgt)

if not exists(datapath + '/' + 'iter_2/window_run'):
    mkdir(datapath + '/' 'iter_2/window_run')

window_grid = [10,20,30,40,50]
image_stride = 10

for cv_name, cv in ncv.cv.items():
    for image_window in window_grid:
        trnparams = TrnParamsConvolutional(prefix="convnet_run_slide",
                                           input_shape=(image_window, 400, 1), epochs=30,
                                           layers=[
                                               ["Conv2D", {"filters": 6,
                                                           "kernel_size": (9, 5),
                                                           "strides": 1,
                                                           "data_format": "channels_last",
                                                           "padding": "valid"
                                                           }
                                                ],
                                               ["Activation", {"activation": "tanh"}],
                                               ["MaxPooling2D", {"pool_size": (2, 4),
                                                                 "padding": "valid",
                                                                 "strides": 1}
                                                ],
                                               ["Flatten", {}],
                                               ["Dense", {"units": 80}],
                                               ["Activation", {"activation": "tanh"}],
                                               ["Dense", {"units": 4}],
                                               ["Activation", {"activation": "softmax"}]
                                           ],
                                           loss="categorical_crossentropy")

        run_info = SonarRunsInfo(audiodatapath + '/' + database)

        def transform_fn(all_data, all_trgt, index_info, info):
            if info == 'train':
                stride = image_stride
            else:
                stride = image_window
            return lofar2image(all_data=all_data,
                               all_trgt=all_trgt,
                               index_info=index_info,
                               window_size=image_window,
                               stride=stride,
                               run_indices_info=run_info)

        cvt = ConvolutionTrainFunction()
        cvt.loadModels([trnparams], KerasModel)
        cvt.loadData(dataset)
        cvt.loadFolds(cv)
        cvt.train(transform_fn=transform_fn, preprocessing_fn=None,
                  fold_mode=cv_name, fold_balance='class_weights',
                  verbose=(1, 1, 1))
