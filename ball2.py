import vtk
import numpy as np
import math


class MySphere:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
        self.velocity = [10, 0, 0]  # la esfera cae, por eso tiene una velocida hacia abajo
        self.last_velocity = [0, 0, 0]
        self.actor = None


class MyFloor:
    def __init__(self, pos, height):
        self.pos = pos
        self.height = height
        self.velocity = np.array([0, 0, 0])
        self.actor = None

class MyPared:
    def __init__(self, pos, height):
        self.pos = pos
        self.height = height
        self.velocity = np.array([0, 0, 0])
        self.actor = None

largo = 20
height = 3
sphere = MySphere([0,0+height, 0], 2)
floor = MyFloor([0, 0, 0], 1)

pared = MyPared([0,1,20], 3)

pared2 = MyPared([0,1,-20], 3)

pared3 = MyPared([largo,1,0], 3)

pared4 = MyPared([-largo,1,0], 3)

time = 0
g = 9



def set_initial_position():
    sphere_actor.SetPosition(sphere.pos[0], sphere.pos[1], sphere.pos[2])
    floor_actor.SetPosition(floor.pos[0], floor.pos[1], floor.pos[2])

    pared_actor.SetPosition(pared.pos[0], pared.pos[1], pared.pos[2])
    pared2_actor.SetPosition(pared2.pos[0], pared2.pos[1], pared2.pos[2])
    pared3_actor.SetPosition(pared3.pos[0], pared3.pos[1], pared3.pos[2])
    pared4_actor.SetPosition(pared4.pos[0], pared4.pos[1], pared4.pos[2])


def callback_func(caller, timer_event):
    global time
    print("velocity", sphere.velocity, "last velocity", sphere.last_velocity)
    # print("pos", sphere.pos, "\n")

    sphere.pos[0] = sphere.pos[0] + sphere.velocity[0] * time
    sphere.last_velocity[0] = sphere.velocity[0]
    #if(sphere.pos[0] - sphere.radius<-largo/2+height/2):
        #sphere.velocity[0] = abs(sphere.velocity[0] / 1.3)  # con cada rebote, se libera energia(calor, vibracion, etc) y se pierde velocidad
    #else:
    sphere.velocity[0] = sphere.velocity[0] - g * time
    if(sphere.velocity[0]<0):
        time =0
    sphere.actor.SetPosition(sphere.pos)
    time += 0.001
    render_window.Render()


# source
source1 = vtk.vtkSphereSource()
source1.SetThetaResolution(50)
source1.SetRadius(sphere.radius)
source1.Update()

source2 = vtk.vtkCubeSource()
source2.SetXLength(40)
source2.SetYLength(floor.height)
source2.SetZLength(40)
source2.Update()

source3 = vtk.vtkCubeSource()
source3.SetXLength(40)
source3.SetYLength(pared.height)
source3.SetZLength(1)
source3.Update()

source4 = vtk.vtkCubeSource()
source4.SetXLength(40)
source4.SetYLength(pared2.height)
source4.SetZLength(1)
source4.Update()

source5 = vtk.vtkCubeSource()
source5.SetXLength(1)
source5.SetYLength(pared3.height)
source5.SetZLength(41)
source5.Update()

source6 = vtk.vtkCubeSource()
source6.SetXLength(1)
source6.SetYLength(pared4.height)
source6.SetZLength(41)
source6.Update()


# mapper
sphere_mapper = vtk.vtkPolyDataMapper()
sphere_mapper.SetInputData(source1.GetOutput())

floor_mapper = vtk.vtkPolyDataMapper()
floor_mapper.SetInputData(source2.GetOutput())

pared_mapper = vtk.vtkPolyDataMapper()
pared_mapper.SetInputData(source3.GetOutput())

pared2_mapper = vtk.vtkPolyDataMapper()
pared2_mapper.SetInputData(source4.GetOutput())

pared3_mapper = vtk.vtkPolyDataMapper()
pared3_mapper.SetInputData(source5.GetOutput())

pared4_mapper = vtk.vtkPolyDataMapper()
pared4_mapper.SetInputData(source6.GetOutput())



# actor
sphere_actor = vtk.vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(0, 1, 0.0)
# sphere_actor.GetProperty().SetOpacity(0.5)
sphere.actor = sphere_actor

floor_actor = vtk.vtkActor()
floor_actor.SetMapper(floor_mapper)
floor_actor.GetProperty().SetColor(1, 1, 0.0)
# sphere_actor.GetProperty().SetOpacity(0.7)
floor.actor = floor_actor

pared_actor = vtk.vtkActor()
pared_actor.SetMapper(pared_mapper)
pared_actor.GetProperty().SetColor(0, 1, 0.0)
# sphere_actor.GetProperty().SetOpacity(0.7)
pared.actor = pared_actor

pared2_actor = vtk.vtkActor()
pared2_actor.SetMapper(pared2_mapper)
pared2_actor.GetProperty().SetColor(0, 1, 0.0)
# sphere_actor.GetProperty().SetOpacity(0.7)
pared2.actor = pared2_actor

pared3_actor = vtk.vtkActor()
pared3_actor.SetMapper(pared3_mapper)
pared3_actor.GetProperty().SetColor(0, 1, 0.0)
# sphere_actor.GetProperty().SetOpacity(0.7)
pared3.actor = pared3_actor

pared4_actor = vtk.vtkActor()
pared4_actor.SetMapper(pared4_mapper)
pared4_actor.GetProperty().SetColor(0, 1, 0.0)
# sphere_actor.GetProperty().SetOpacity(0.7)
pared4.actor = pared4_actor



# camera
camera = vtk.vtkCamera()
camera.SetFocalPoint(0,0,0)
camera.SetPosition(100,150,150)


# renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(sphere_actor)
renderer.AddActor(floor_actor)
renderer.AddActor(pared_actor)
renderer.AddActor(pared2_actor)
renderer.AddActor(pared3_actor)
renderer.AddActor(pared4_actor)

renderer.SetActiveCamera(camera)

# renderWindow
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Simple VTK scene")
render_window.SetSize(800, 800)
render_window.AddRenderer(renderer)

# interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()

set_initial_position()

interactor.CreateRepeatingTimer(1)
interactor.AddObserver("TimerEvent", callback_func)
interactor.Start()