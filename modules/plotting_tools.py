
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pickle



class plotter_3d(object):
    def __init__(self, output_file="", parallel=False, interactive=False):
        
        self.output_file=output_file
        self.parallel=parallel
        self.interactive=interactive
        self.data=None
        
        
    def save_binary(self, outfilename):
        with open(outfilename,'w') as outfile:
            pickle.dump(self.output_file,outfile)
            pickle.dump(self.parallel,outfile)
            pickle.dump(self.interactive,outfile)
            pickle.dump(self.data,outfile)
        
    def load_binary(self, infilename):
        with open(infilename,'r') as infile:
            self.output_file = pickle.load(infile)
            self.parallel    = pickle.load(infile)
            self.interactive = pickle.load(infile)
            self.data        = pickle.load(infile)
    
    def set_data(self, x, y, z, e, c=None):
        self.data={'x' : x,
                   'y' : y,
                   'z' : z,
                   'e' : e,
                   'c' : c}
    
    def plot3d(self, e_scaling='sqrt', cut=None):
        
        if self.data is None:
            raise Exception("plot3d: no data")

        x, y, z, e, c = self.data['x'], self.data['y'], self.data['z'], self.data['e'], self.data['c']

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #switch for standard CMS coordinates
        
        zs = np.reshape(x,[1,-1])
        ys = np.reshape(y,[1,-1])
        xs = np.reshape(z,[1,-1])
        es = np.reshape(e,[1,-1])
        #flattened_sigfrac = np.reshape(truth_list[0][:,:,:,0],[1,-1])
        #ax.set_axis_off()
        if e_scaling is not None and e_scaling == 'sqrt':
            es = np.sqrt(np.abs(e))
        else:
            es=e
        if c is None:
            c=np.log(np.log(es+1)+1)
        ax.scatter(xs=xs, ys=ys, zs=zs, c=c, s=np.exp(e)-1.)
        fig.savefig(self.output_file)
        if self.interactive:
            plt.show()
        plt.close()
        
        
    def _plot(self):
        #return
        pred_coords = predict_output_list[0][0]
        #print('pred_coords',pred_coords.shape)
        orig_coords = model_input_list[0][0]
        fig = plt.figure()
        ax = fig.add_subplot(121, projection='3d')
        xs = np.reshape(pred_coords[:,-1],[1,-1])
        ys = np.reshape(pred_coords[:,-2],[1,-1])
        zs = np.reshape(pred_coords[:,-3],[1,-1])
        #flattened_sigfrac = np.reshape(truth_list[0][:,:,:,0],[1,-1])
        #ax.set_axis_off()
        ax.scatter(xs=xs, ys=ys, zs=zs, 
                   c=np.reshape(orig_coords, [1,-1]), s=5*np.reshape(orig_coords, [1,-1]),
                   cmap='YlOrRd')#,c=flattened_sigfrac)
        ax.view_init(30, self.glob_counter)
        
        if self.glob_anglecounter>360:
            self.glob_anglecounter=0
        fig.add_subplot(122)
        plt.imshow(orig_coords[:,:,0])
        fig.savefig(outputname)
        plt.close()
            
            
        