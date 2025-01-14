# ----------------------------------------------
# Script Recorded by ANSYS Electronics Desktop Version 2020.1.0
# 14:23:14  May 06, 2020
# ----------------------------------------------
from pyaedt import Hfss

# Launch HFSS and create a new project
hfss = Hfss(specified_version="2024.2", new_desktop_session=True)
hfss.save_project("Microstrip_Antenna")

# define parameters
substrate_thickness = "3mm"
substrate_material= "FR4_epoxy"
patch_length = "30mm"
patch_width = "20mm"
feed_line_width = "2mm"
feed_line_length = "15mm"
frequency = "2.4GHz"

# Create the substrate 
hfss.modeler.create_box([0,0,0], [patch_length, patch_width,substrate_thickness], name="Substrate", matname=substrate_material)

# create the ground plane 
hfss.modeler.create_rectangle(position=[0,0,0], dimension_list =[patch_length, patch_width], name="GroundPlane", matname="copper")
hfss.assign_perfect_e_to_faces("GroundPlane")

# Create the patch 
hfss.modeler.create_rectangle(position=[0,0,substrate_thickness], dimension_list=[patch_length, patch_width].name="Patch", matname="Copper")

# Create the feedline 
hfss.modeler.create_rectangle(position=[(patch_length-feed_line_width)/2, -feed_line_length, substrate_thickness], dimension_list=[feed_line_width, feed_line_length], name="feedline", matname="Copper")

# assign port
hfss.create_wave_port_between_objects("FeedLine", "GroundPlane", axisdir="X", name="Port1")

# Set simulation boundaries 
hfss.assign_radiation_boundary_to_faces("Patch")

# Setup solution
setup = hfss.create_setup("Setup1")
setup.props["Frequency"] = frequency
setup.props["MaxDeltaS"] = 0.02 # Convergence criteria 
hfss.create_frequency_sweep(setupname="Setup1", unit="GHz", freqstart=1, freqstop=5, step_size=0.1)

# validate and sun simulation
hfss.validate_project()
hfss.analyze_all()

# Post processing 
s_parameters = hfss.post.get_solution_data(expression="S(Port1, Port1)")
s_parameter.plot()
hfss.save_project()
hfss.close_desktop()


