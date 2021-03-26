import vtk
import math

sphere_pos = [0,2,0]
floor_pos = [0,0,0]
largo = 40
ancho = 40
radio = 2
velocity_x=0.1
velocity_z=0.2
direction_x = 1
direction_z = 1
ax =-0.001
az =-0.001
time = 0
def set_initial_position():
    sphere_actor.SetPosition(sphere_pos)
    floor_actor.SetPosition(floor_pos)

def callback_func2(caller, timer_event):
    global direction_x,direction_z,ax,az,velocity_x,velocity_z

    x,y,z=sphere_actor.GetPosition()
    if(x<-largo/2 or x>largo/2):
        direction_x*=-1
    if(z<-ancho/2 or z>ancho/2):
        direction_z*=-1
    vx=max(0,direction_x*velocity_x)
    vz=max(0,direction_z*velocity_z)
    velocity_x+=ax
    velocity_z+=az

    sphere_pos[0] += vx
    sphere_pos[2] += vz
    print(vx,vz)
    sphere_actor.SetPosition(sphere_pos)
    render_window.Render()
class MySphere:
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
        self.velocity = [0, 10, 0]  # la esfera cae, por eso tiene una velocida hacia abajo
        self.last_velocity = [0, -10, 0]
        self.actor = None

def callback_func(caller, timer_event):
    global time
    print("velocity", sphere.velocity, "last velocity", sphere.last_velocity)
    sphere.pos[0] += sphere.velocity[0] * time
    sphere.last_velocity[0] = sphere.velocity[0]
    if (sphere.pos[0] - sphere.radius) < (floor.pos[0] + floor.height / 2):
        sphere.velocity[0] = abs(sphere.velocity[0] / 1.3)  # con cada rebote, se libera energia(calor, vibracion, etc) y se pierde velocidad
    else:
        sphere.velocity[0] = sphere.velocity[0] - g * time

        if sphere.last_velocity[0] * sphere.velocity[1] < 0:  # si cambio la dirección de la velocidad, cuando empieza a caer
            # print("\nrestart time\n")
            time = 0

    sphere.actor.SetPosition(sphere.pos[0], sphere.pos[1], sphere.pos[2])
    time += 0.001
    render_window.Render()

sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(50)
sphere.SetRadius(radio)
sphere.Update()

floor = vtk.vtkCubeSource()
floor.SetXLength(largo)
floor.SetYLength(1)
floor.SetZLength(ancho)
floor.Update()

# mapper
sphere_mapper = vtk.vtkPolyDataMapper()
sphere_mapper.SetInputData(sphere.GetOutput())
floor_mapper = vtk.vtkPolyDataMapper()
floor_mapper.SetInputData(floor.GetOutput())


#actor
sphere_actor = vtk.vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(0, 1, 0.0)

floor_actor = vtk.vtkActor()
floor_actor.SetMapper(floor_mapper)
floor_actor.GetProperty().SetColor(1, 1, 0.0)

#camera
camera = vtk.vtkCamera()
camera.SetFocalPoint(0,0,0)
camera.SetPosition(0,largo*2,ancho*2)

#renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(sphere_actor)
renderer.AddActor(floor_actor)
renderer.SetActiveCamera(camera)

#renderWindow
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Simple VTK scene")
render_window.SetSize(800, 800)
render_window.AddRenderer(renderer)

#interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()

set_initial_position()

interactor.CreateRepeatingTimer(1)
interactor.AddObserver("TimerEvent", callback_func)
interactor.Start()

