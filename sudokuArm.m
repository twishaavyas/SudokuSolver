robot = robotics.RigidBodyTree('DataFormat','column','MaxNumBodies',3);
L1 = 9;
L2 = 9;
L3 = 9;

body = robotics.RigidBody('link1');
joint = robotics.Joint('joint1', 'revolute');
setFixedTransform(joint,trvec2tform([0 0 0]));
joint.JointAxis = [0 0 1];
body.Joint = joint;
addBody(robot, body, 'base');

body = robotics.RigidBody('link2');
joint = robotics.Joint('joint2','revolute');
setFixedTransform(joint, trvec2tform([L1,0,0]));
joint.JointAxis = [0 0 1];
body.Joint = joint;
addBody(robot, body, 'link1');

body = robotics.RigidBody('link3');
joint = robotics.Joint('joint3','revolute');
setFixedTransform(joint, trvec2tform([L2,0,0]));
joint.JointAxis = [0 0 1];
body.Joint = joint;
addBody(robot, body, 'link2');

body = robotics.RigidBody('tool');
joint = robotics.Joint('fix1','fixed');
setFixedTransform(joint, trvec2tform([L3, 0, 0]));
body.Joint = joint;
addBody(robot, body, 'link3');

showdetails(robot)

%t = (0:0.2:10)'; % Time



%center = [0.3 0.1 0];

%radius = 0.15;
%theta = t*(2*pi/t(end));

 commandStr = 'python E:/Robotics/sudoku/project/browseupload.py';
 [status, commandOut] = system(commandStr);
 status
 commandOut
 if status==0
     fprintf('squared result is %d\n',str2num(commandOut));
 end

sudoku = '075000096030100075020970004740000308089000460306000017200063080590008020860000540';
i = -9;
j = 9;
starting_index = 1;
while i < 10
    while j > -10
        initial_x= i;
        initial_y = j;
        number = sudoku(starting_index);
        i = i + 2;
        j = j - 2;
        sudoku_plot(initial_x, initial_y, number, robot);
    end
end

function sudoku_plot(x, y, number, robot)
allpoints = trace_number(x, y, number);
allpoints;
count = 20;
%points = center + radius*[cos(theta) sin(theta) zeros(size(theta))]


q0 = homeConfiguration(robot);
ndof = length(q0);
qs = zeros(size(count,1), ndof);
ik = robotics.InverseKinematics('RigidBodyTree', robot);
weights = [0, 0, 0, 1, 1, 0];
endEffector = 'tool';

qInitial = q0; % Use home configuration as the initial guess
for i = 1:count
    % Solve for the configuration satisfying the desired end effector
    % position
    
    point = allpoints(i,:);
    qSol = ik(endEffector,trvec2tform(point),weights,qInitial);
    % Store the configuration
    qs(i,:) = qSol;
    % Start from prior solution
    qInitial = qSol;
end

figure
show(robot,qs(1,:)');
view(2)
ax = gca;
ax.Projection = 'orthographic';
hold on
plot(allpoints(:,1),allpoints(:,2),'k')
axis([-18 18 -18 18])

framesPerSecond = 15;
r = robotics.Rate(framesPerSecond);
for i = 1: size(allpoints,1)
    show(robot,qs(i,:)','PreservePlot',false);
    drawnow
    waitfor(r);
end

end

function allpoints = trace_number(c1,c2,num)
    number = getNum(num);
    x = number(1,:)+ c1*ones(1,size(number,2));
    x
    c = length(x);
    y = number (2,:) + c2*ones(1,size(number,2));
    y
    allpoints = [];
    for i =1: c - 1
        
        p = [transpose(linspace(x(1,i),x(1,i+1), 10)) transpose(linspace(y(1,i),y(1,i+1), 10))];
        allpoints = [allpoints ; p];
    end 
    allpoints = [allpoints zeros(size(allpoints,1),1)]
end

function number = getNum(num)
    if(num == '1')
        x = [1 1 1];
        y = [1.5 1 0.5];
        number = [x;y];
    end
    
    if(num == '2')
       x = [0.5 1.5 1.5 0.5 0.5 1.5];
       y = [1.5 1.5 1 1 0.5 0.5];
       number = [x;y];
    end
       
   if(num == '3')
       x =[0.5 1.5 1.5 0.5 1.5 1.5 0.5];
       y = [1.5 1.5 1 1 1 0.5 0.5];
       number = [x;y];
   end
   
   if (num == '4')
       x = [0.5 0.5 1.5 1.5 1.5];
       y = [1.5 1 1 1.5 0.5];
       number = [x;y];
   end
       
   if (num == '5')
       x = [1.5 0.5 0.5 1.5 1.5 0.5];
       y = [1.5 1.5 1 1 0.5 0.5];
       number = [x;y];
   end
   
   if (num =='6')
       x = [1.5 0.5 0.5 1.5 1.5 0.5]
       y = [1.5 1.5  0.5 0.5 1 1]
       number = [x;y];
   end
   
   if (num == '7')
       x = [0.5 1.5 1.5];
       y = [1.5 1.5 0.5];
       number = [x;y];
   end
   
   if(num == '8')
       x = [0.5 1.5 1.5 0.5 0.5 1.5 1.5 0.5 0.5];
       y = [1.5 1.5 1 1 0.5 0.5 1 1 1.5]
       number = [x;y];
   end
       
   if (num == '9')
       x = [1.5 0.5 0.5 1.5 1.5 0.5]
       y = [1 1 1.5 1.5 0.5 0.5]
       number = [x;y];
   end
   
   if(num == '0')
       x = [0.5 1 1.5];
       y = [1 1 1];
       number = [x;y]
   end
       
end