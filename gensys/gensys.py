from sympy import symbols
import sympy as sym
import numpy as np
import matplotlib as plt


class Gensys:
    def __init__(self,parameters:str, variables:str, shocks:str,equations):
        ''' 
        variables: str
        string of variables separated by commas.
        '''
        #self.vars = {v:symbols(v) for v in variables.replace(" ", "").split(',')}
        self.vars = variables
        self.n_var = len(self.vars)
        self.shocks = {s:symbols(s) for s in shocks.replace(" ", "").split(',')}
        self.n_shocks = len(self.shocks)
        self.parameters = {p:symbols(p) for p in parameters.replace(" ", "").split(',')}
        self.system_symbolic = None
        self.system_numeric = None
        self.matrix_solution = None
        self.calibration = None
        #self.equations = {Eq(*[eval(i) for i in eq.split('=')]) for eq in equations}
        pass

    def get_matrices(self,equations, var_, z, eta):
        vars = self.vars
        Gamma0,_ = sym.linear_eq_to_matrix(equations, vars)
        Gamma1,_ = sym.linear_eq_to_matrix(_,var_)
        Psi, _ = sym.linear_eq_to_matrix(_, z)
        Eta, C = sym.linear_eq_to_matrix(_, eta)
        Psi = -Psi
        C = -C
        self.system_symbolic={'Gamma0':Gamma0, 'Gamma1':Gamma1,'Psi':Psi, 'Eta':Eta, 'C':C}
        pass
        
    def calibrate(self,calibration):
        self.calibration = calibration
        Gamma0 = self.system_symbolic['Gamma0'].subs(calibration)
        Gamma1 = self.system_symbolic['Gamma1'].subs(calibration)
        Psi = self.system_symbolic['Psi'].subs(calibration)
        Eta = self.system_symbolic['Eta']
        C = self.system_symbolic['C'].subs(calibration)
        self.system_numeric = {'Gamma0':Gamma0, 'Gamma1':Gamma1,'Psi':Psi, 'Eta':Eta, 'C':C}
        pass

    def solve(self):
        return self._solve(**self.system_numeric)
     
    def _solve(self, Gamma0, Gamma1, Psi, Eta, C):
        Gamma0_inv=Gamma0.inv()
        Gamma1, C, Psi, Eta = Gamma0_inv@Gamma1, Gamma0_inv@C, Gamma0_inv@Psi, Gamma0_inv@Eta 
        P, Lambda = Gamma1.diagonalize()
        ind = list(np.argsort(np.abs(np.diag(np.abs(Lambda)))))
        Lambda = sym.diag(*[Lambda[i,i] for i in ind])
        n_s = len([Lambda[i,i] for i in range(Lambda.rows) if np.abs(Lambda[i,i])<1])
        n_u = Lambda.rows-n_s        
        P=P.permute_cols(ind)  
        P = np.array(P).astype(np.complex128) 
        P_inv = np.linalg.inv(P)
        Lambda_S=Lambda[:n_s,:n_s]
        Lambda_U=Lambda[n_s:,n_s:]
        Theta_1 = P[:,:n_s]@Lambda_S@P_inv[:n_s,:]
        Theta_c = (P[:,:n_s]@P_inv[:n_s,:]+P[:,n_s:]@(sym.eye(n_u)-Lambda_U)@P_inv[n_s:,:])@C
        Phi = P_inv[:n_s,:]@Eta@(P_inv[n_s:,:]@Eta).inv()
        Theta_z = (P[:,:n_s]@P_inv[:n_s,:]-P[:,:n_s]@Phi@P_inv[n_s:,:])@Psi
        Theta_1 = np.real(np.array(Theta_1).astype(np.complex64))
        Theta_c = np.real(np.array(Theta_c).astype(np.complex64))
        Theta_z = np.real(np.array(Theta_z).astype(np.complex64)) 
        self.matrix_solution={'Theta_1':Theta_1,'Theta_c':Theta_c, 'Theta_z':Theta_z}
    
    def impulse_response(self, z:np.array, T:int = 25):
        '''
        z: initial shock
        '''
        n_var = self.n_var
        Theta_1 = self.matrix_solution['Theta_1']
        Theta_c = self.matrix_solution['Theta_c']
        Theta_z = self.matrix_solution['Theta_z']
        z_t = np.zeros((T+1,self.n_shocks))
        z_t[1] = z
        y_t = np.zeros((T+1,n_var))
        t=np.arange(-1,T)
        for i in range(1,T+1):
            y_t[i]=Theta_1@y_t[i-1]+Theta_c.flatten()+Theta_z@z_t[i]

        max_cols=3
        fig,ax=plt.subplots(nrows=(n_var-1)//max_cols+1,ncols=min(n_var,max_cols),
                            figsize=(3*5,5*((n_var-1)//max_cols+1)))
        for i in range(n_var):
            ax[i//max_cols,i%max_cols].plot(t,y_t[:,i])
            ax[i//max_cols,i%max_cols].set(title=f'${self.vars[i]}$',xlabel='t')
        fig.show()