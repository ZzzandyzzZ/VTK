import vtk
import math

sphere_pos = [0,2,0]
floor_pos = [0,0,0]
largo = 40
ancho = 40
vx=1
vz=2
ax =-0.001
az =-0.001
def set_initial_position():
    sphere_actor.SetPosition(sphere_pos)
    floor_actor.SetPosition(floor_pos)

def callback_func(caller, timer_event):
    global vx,vz,ax,az
    sphere_pos[0] += vx
    sphere_pos[2] += vz
#    vx+=ax
#    vz+=az
#    if(vx<0):vx=0
#    if(vz<0):vz=0
    
    sphere_actor.SetPosition(sphere_pos)
    render_window.Render()
    x,y,z=sphere_actor.GetPosition()
    if(x<-largo/2 or x>largo/2):
        vx*=-1
#        ax*=-1
    if(z<-ancho/2 or z>ancho/2):
        vz*=-1
#        az*=-1
# source
sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(50)
sphere.SetRadius(2)
sphere.Update()

floor = vtk.vtkCubeSource()
floor.SetXLength(40)
floor.SetYLength(1)
floor.SetZLength(40)
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

interactor.CreateRepeatingTimer(20)
interactor.AddObserver("TimerEvent", callback_func)
interactor.Start()

