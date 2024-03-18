# Define AWS provider
provider "aws" {
  region = "us-west-2"  # Change to your desired region
}

# Create a VPC
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"  # Change to your desired CIDR block
  enable_dns_support = true
  enable_dns_hostnames = true
}

# Create a subnet within the VPC
resource "aws_subnet" "my_subnet" {
  vpc_id     = aws_vpc.my_vpc.id
  cidr_block = "10.0.1.0/24"  # Change to your desired CIDR block within the VPC
}

# Create a security group for EC2 instances
resource "aws_security_group" "instance_sg" {
  name        = "instance_sg"
  description = "Allow inbound traffic to EC2 instances"
  vpc_id      = aws_vpc.my_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Add more ingress rules as needed for your application
}

# Launch EC2 instances
resource "aws_instance" "my_instance" {
  count         = 2  # Change to the desired number of instances
  ami           = "ami-12345678"  # Change to your desired AMI
  instance_type = "t2.micro"      # Change to your desired instance type

  subnet_id     = aws_subnet.my_subnet.id
  key_name      = "my_key_pair"   # Change to your key pair name
  security_groups = [aws_security_group.instance_sg.name]

  # You can add more configurations here like user_data, tags, etc.
}

# Create an Application Load Balancer (ALB)
resource "aws_lb" "my_alb" {
  name               = "my-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [aws_subnet.my_subnet.id]

  enable_deletion_protection = false  # Change as needed
}

# Create a target group for the ALB
resource "aws_lb_target_group" "my_target_group" {
  name     = "my-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.my_vpc.id

  health_check {
    path                = "/"
    port                = "80"
    protocol            = "HTTP"
    timeout             = 5
    interval            = 30
    unhealthy_threshold = 2
    healthy_threshold   = 2
  }
}

# Attach instances to the target group
resource "aws_lb_target_group_attachment" "my_target_group_attachment" {
  count = length(aws_instance.my_instance)
  target_group_arn = aws_lb_target_group.my_target_group.arn
  target_id        = aws_instance.my_instance[count.index].id
  port             = 80
}

# Create a security group for ALB
resource "aws_security_group" "alb_sg" {
  name        = "alb_sg"
  description = "Allow inbound traffic to ALB"
  vpc_id      = aws_vpc.my_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create WAF Web ACL
resource "aws_waf_web_acl" "example" {
  name        = "example-web-acl"
  metric_name = "example-web-acl-metric"

  default_action {
    allow {}
  }

  # Define your rules here
}

# Create WAF Rule
resource "aws_waf_rule" "example" {
  name        = "example-rule"
  metric_name = "example-rule-metric"

  predicates {
    data_id = aws_waf_ipset.example.id
    negated = false
    type    = "IPMatch"
  }
}

# Create WAF IP Set
resource "aws_waf_ipset" "example" {
  name        = "example-ipset"
  ip_set_descriptors {
    type  = "IPV4"
    value = "192.0.7.0/24"
  }
}

# Attach WAF ACL to the ALB
resource "aws_waf_web_acl_association" "example" {
  resource_arn = aws_lb.my_alb.arn
  web_acl_id   = aws_waf_web_acl.example.id
}
