#include <GL/freeglut.h>  // Use freeglut instead of GLUT
#include <cmath>

// Constants
const int WINDOW_WIDTH = 800;
const int WINDOW_HEIGHT = 600;
const float ROD_LENGTH = 200.0f;
const float BALL_RADIUS = 20.0f;
const float GRAVITY = 9.81f;
const float TIME_STEP = 0.01f;

// Variables
float theta = 45.0f;  // Initial angle in degrees
float thetaVelocity = 0.0f;
float thetaAcceleration = 0.0f;

// Function to update the pendulum state
void updatePendulum() {
  thetaAcceleration = (-GRAVITY / ROD_LENGTH) * sin(theta * M_PI / 180.0f);
  thetaVelocity += thetaAcceleration * TIME_STEP;
  theta += thetaVelocity * TIME_STEP;
}

// Function to render the pendulum
void renderPendulum() {
  glClear(GL_COLOR_BUFFER_BIT);
  glLoadIdentity();
  
  // Draw the rod
  glColor3f(1.0f, 1.0f, 1.0f);
  glBegin(GL_LINES);
  glVertex2f(WINDOW_WIDTH / 2, WINDOW_HEIGHT);
  glVertex2f(WINDOW_WIDTH / 2 + ROD_LENGTH * sin(theta * M_PI / 180.0f), WINDOW_HEIGHT - ROD_LENGTH * cos(theta * M_PI / 180.0f));
  glEnd();
  
  // Draw the ball
  glTranslatef(WINDOW_WIDTH / 2 + ROD_LENGTH * sin(theta * M_PI / 180.0f), WINDOW_HEIGHT - ROD_LENGTH * cos(theta * M_PI / 180.0f), 0.0f);
  glColor3f(0.0f, 0.0f, 1.0f);
  glBegin(GL_TRIANGLE_FAN);
  for (int i = 0; i < 360; i++) {
    float thetaRad = i * M_PI / 180.0f;
    float x = BALL_RADIUS * cos(thetaRad);
    float y = BALL_RADIUS * sin(thetaRad);
    glVertex2f(x, y);
  }
  glEnd();
  
  glFlush();
}

// Function to handle window resize event
void reshape(int width, int height) {
  glViewport(0, 0, width, height);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluOrtho2D(0, width, 0, height);
  glMatrixMode(GL_MODELVIEW);
}

// Function to update and render the pendulum
void updateAndRender(int value) {
  updatePendulum();
  renderPendulum();
  glutTimerFunc(10, updateAndRender, 0);
}

int main(int argc, char** argv) {
  // Initialize OpenGL and GLUT
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
  glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT);
  glutCreateWindow("Pendulum Simulator");
  
  // Register callback functions
  glutReshapeFunc(reshape);
  glutTimerFunc(10, updateAndRender, 0);
  
  // Enter the main loop
  glutMainLoop();
  
  return 0;
}
