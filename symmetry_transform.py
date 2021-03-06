from symmetry_functions import G1,G2,G3,G4,G5
import numpy as np

def symmetryTransform(G_funcs, xyz_i):
    """
    Input:
    x,y,z-coordinates of N particles that make up
    the neighbor-list of particle i.
        [[x1 y1 z1]
         [x2 y2 z2]
         [x3 y3 z3]
         [x4 y4 z4]]
    G_funcs : List of lists to be used.
        [G1, G2, G3, G4, G5]

    Output:
    G1,G2,...,G5: [g11 g12 g13 ... g1N, g21 g22 ... g2N , ... , g5N]
    Some combination of G's are usually used (not all)

    Definitions of G1,...,G5, see:
        "Atom-centered symmetry functions for constructing high-dimensional neural network potentials"
        by Jorg Behler, The Journal of Chemical Physics 134, 074106 (2011).

    ----------------
    Symm |   Vars
    ----------------
    G1   |   rc
    G2   |   rc, rs, eta
    G3   |   rc, kappa
    G4   |   rc, eta, zeta, lambda_c
    G5   |   rc, eta, zeta, lambda_c
    """

    xyz  = xyz_i
    r    = np.linalg.norm(xyz,axis=1)
    G_output = []

    if G_funcs[0] != 0:
        """
        ### This is G1 ###
        ### Variables: ###
            - rc
        """
        G = 0
        N = G_funcs[G][0]
        for n in range(N):
            values = G_funcs[G][1]
            rc     = float(values[n,0])
            G_output.append( G1(r, rc) )
    if G_funcs[1] != 0:
        """
        ### This is G2 ###
        ### Variables: ###
            - rc, rs, eta
        """
        G = 1
        N = G_funcs[G][0]
        for n in range(N):
            values = G_funcs[G][1]
            rc     = float(values[n,0])
            rs     = float(values[n,1])
            eta    = float(values[n,2])
            G_output.append( G2(r, rc, rs, eta) )
    if G_funcs[2] != 0:
        """
        ### This is G3 ###
        ### Variables:
            -rc, kappa
        """
        G = 2
        N = G_funcs[G][0]
        for n in range(N):
            values = G_funcs[G][1]
            rc     = float(values[n,0])
            kappa  = float(values[n,1])
            G_output.append( G3(r, rc, kappa) )
    if G_funcs[3] != 0:
        """
        ### This is G4 ###
        ### Variables:
            - rc, eta, zeta, lambda_c
        """
        G = 3
        N = G_funcs[G][0]
        for n in range(N):
            values   = G_funcs[G][1]
            rc       = float(values[n,0])
            eta      = float(values[n,1])
            zeta     = float(values[n,2])
            lambda_c = float(values[n,3])
            G_output.append( G4(xyz, rc, eta, zeta, lambda_c) )
            # print rc, eta, zeta, lambda_c
    if G_funcs[4] != 0:
        """
        ### This is G5 ###
        ### Variables:
            - rc, eta, zeta, lambda_c
        """
        G = 4
        N = G_funcs[G][0]
        for n in range(N):
            values   = G_funcs[G][1]
            rc       = float(values[n,0])
            eta      = float(values[n,1])
            zeta     = float(values[n,2])
            lambda_c = float(values[n,3])
            G_output.append( G5(xyz, rc, eta, zeta, lambda_c) )
    return np.array(G_output)

def symmetryTransformBehler(all_params_list, xyz):
    r        = np.linalg.norm(xyz, axis=1)
    G_output = []
    for cur_param_set in all_params_list:
        if cur_param_set[0] == 2:
            """
            ### This is G2 ###
            ### Variables: ###
                - rc, rs, eta
            """
            eta, rc, rs = cur_param_set[1:4] # notice not same order
            G_output.append( G2(r, float(rc), float(rs), float(eta)) )
        elif cur_param_set[0] == 4:
            """
            ### This is G4 ###
            ### Variables:
                - rc, eta, zeta, lambd
            """
            eta, rc, zeta, lambd = cur_param_set[1:5] # notice not same order
            G_output.append( G4(xyz, float(rc), float(eta), float(zeta), float(lambd)) )
        elif cur_param_set[0] == 5:
            """
            ### This is G5 ###
            ### Variables:
                - rc, eta, zeta, lambd
            """
            eta, rc, zeta, lambd = cur_param_set[1:5] # notice not same order
            G_output.append( G5(xyz, float(rc), float(eta), float(zeta), float(lambd)) )
        else:
            print "Symm.func. number:", cur_param_set[0], "was not understood. Input 2 or 4..."
    return np.array(G_output)



if __name__ == '__main__':
    print "This will perform tests of the Stillinger Weber potential"
    print "-------------------------------"

    r_low     = 0.85
    r_high    = 1.8
    size      = 1       # Note this
    neighbors = 15
    PES       = PES_Stillinger_Weber
    xyz_N     = createXYZ(r_low, r_high, size, neighbors)
    Ep        = potentialEnergyGenerator(xyz_N, PES)
    xyz_i     = xyz_N[:,:,0] # Size is just 1, but anyway..
    G_funcs   = example_generate_G_funcs_input()
    G_vec     = symmetryTransform(G_funcs, xyz_i)

    print "Number of symmetry functions used to describe each atom i:", len(G_vec)
    print "-------------------------------"
    print G_vec
