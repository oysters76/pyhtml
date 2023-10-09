# Python program that converts tree structure to HTML string

class Node(object):
	
	def __init__(self, parentNode, tagName, attributeList, innerText):
		self.parent = parentNode; 
		self.tagName = tagName; 
		self.attributeList = attributeList; 
		self.innerText = innerText; 
		self.children = []; 
		self.isRoot = self.parent == None; 
		self.nodeLevel = -1
		
		if (self.parent != None):	
			self.parent.add_child(self); 
	
	def get_attribute_list_as_string(self):
		result = ""; 
		i = 0
		while (i < (len(self.attributeList)-1)): # ['value', 'foo'] -> value="foo"
			result += self.attributeList[i] + "=" + "\"" + self.attributeList[i+1] + "\" "; 
			i += 2 
			
		if (result != ""):
			result = " " + result; 
		return result;	
	
	def render_node_head(self):
		if (self.isRoot):
			return ""; 
			
		attributeListStr = self.get_attribute_list_as_string();
		return "<" + self.tagName + attributeListStr + ">"; 
	
	def render_node_inner_text(self):
		if (self.isRoot):
			return ""; 
			
		return self.innerText; 
	
	def render_node_foot(self):
		if (self.isRoot):
			return ""; 
			
		return "</" + self.tagName + ">"; 

	def add_child(self, node):
		self.children.append(node); 
	
	def get_children_count(self):
		return len(self.children); 
	
	def get_child(self, index):
		return self.children[index]; 
	
	def __str__(self):
		return self.tagName; 

	def get_level(self):
		if (self.parent == None):
			return 0 
		if (self.nodeLevel >= 0):
			return self.nodeLevel 
		
		currentParent = self.parent; 
		level = 0 
		while not (currentParent == None):
			level += 1 
			currentParent = currentParent.parent; 
		self.nodeLevel = level - 1 # ignore the root node level (so html tag gets a level of 0) 
		return self.nodeLevel;
	
def is_parent(node):
	return node.get_children_count() != None and node.get_children_count() > 0; 

def get_root():
	return Node(None, "", [], ""); 
	
def addToBuffer(text):
	endStr = "\n"; 
	if (text == ""):
		endStr = ""; 
	print(text, end=endStr); 

def setIndentation(currentNode, text, addLevel=0):
	if (text == ""):
		return ""; 
	level = currentNode.get_level() + addLevel; 
	tab = (" " * 4)
	return (tab*level) + text;

def add_to_level_map(levelMap, node):
	if (node.isRoot):
		return levelMap 
	
	level = node.get_level() 
	if (level in levelMap):
		levelMap[level].append(node) 
	else:
		levelMap[level] = [node] 
	return levelMap

def get_stats_data(root):
	maxLevel = 0; 
	deepestNode = root 
	levelMap = {} 

	stack = [root]; 
	while (len(stack) != 0):
		node = stack.pop();
		levelMap = add_to_level_map(levelMap, node); 
		for i in range(len(node.children)):
			stack.append(node.children[i]) 

		if (maxLevel < node.get_level()):
			maxLevel = node.get_level() 
			deepestNode = node; 

	return levelMap, deepestNode, maxLevel;

def get_node_strs(nodes):
	result = " "
	for i in range(len(nodes)):
		result += nodes[i].tagName + " " 
	return result

def create_stat_report(root):
	levelMap, deepestNode, maxLevel = get_stats_data(root) 
	i = 0; 
	totalElements = 0; 
	while (i <= maxLevel):
		if (i not in levelMap):
			continue
		if (len(levelMap[i]) == 0):
			continue 
		totalElements += len(levelMap[i])
		addToBuffer("level " + str(i+1) + ": " + get_node_strs(levelMap[i]) + " (" + str(len(levelMap[i])) +")")
		i += 1
	addToBuffer("TOTAL ELEMENTS: " + str(totalElements))

def renderHTML(root):
	stack = [root]; 
	elementsToClose = []; 
	while (len(stack) != 0):
		currentNode = stack.pop(); # gets me the last element that was recently added 	
		
		
		addToBuffer(setIndentation(currentNode,currentNode.render_node_head())); 
		
		for i in range(currentNode.get_children_count()):
			stack.append(currentNode.get_child(i)); 
		
		isParent = is_parent(currentNode); # figure out whether the node is a parent  
		
		addToBuffer(setIndentation(currentNode, currentNode.render_node_inner_text(), 1)); 
		
		if (isParent):
			elementsToClose.append(currentNode); # append the closing tags to later print
		else:
			addToBuffer(setIndentation(currentNode,currentNode.render_node_foot()));
	
	while (len(elementsToClose) != 0):
		currentNode = elementsToClose.pop(); 
		addToBuffer(setIndentation(currentNode, currentNode.render_node_foot()))

EMMENT_TOKEN_SUB = ">"; # creates a sub node
EMMENT_TOKEN_SIB = "+"; # creates a sibling node

def is_special_token(c):
	return c ==EMMENT_TOKEN_SUB or c == EMMENT_TOKEN_SIB; 



def create_html_element(rootNode, tagName):
	return Node(rootNode, tagName, [], ""); 

def generate_html_from_emment(emment_str):  
	rootNode = get_root(); 
	currentParent = rootNode; 
	currentElem = ""; 
	lastOperation = "";
	for c in emment_str:
		if (is_special_token(c)):
			if (c == EMMENT_TOKEN_SUB):
				currentParent = create_html_element(currentParent, currentElem); 
			if (c == EMMENT_TOKEN_SIB):
				create_html_element(currentParent, currentElem); 
				currentParent = rootNode;
			currentElem = "";
			lastOperation = c;
		if (not is_special_token(c)):
			currentElem += c;
	
	create_html_element(currentParent, currentElem);

	return rootNode; 


rootNode = generate_html_from_emment("nav>ul>li")
renderHTML(rootNode)

# rootNode = get_root(); 
# htmlNode = Node(rootNode, "html", [], ""); 
# bodyNode = Node(htmlNode, "body", [], ""); 
# divNode = Node(bodyNode, "div", ["class", "foo-bar", "style", "background:blue"], ""); 
# paragraphNode = Node(bodyNode, "p", ["style", "background-color:red;color:white"], "This is my text"); 
# paragraphNode2 = Node(divNode, "p", ["style", "color:green", "value", "2"], "This is another text"); 
# subDivNode = Node(paragraphNode2, "div", ["class", "container"], "Hello world!"); 
# h1 = Node(bodyNode, "h1", [], "Hello world!")


# renderHTML(rootNode); # returns an HTML string! 
# create_stat_report(rootNode)
# # print("level of the rootNode is ", rootNode.get_level()); 
# # print("level of the htmlNode is ", htmlNode.get_level()); 
# # print("level of the bodyNode is ", bodyNode.get_level()); 
# # print("level of the paragraphNode2 is ", paragraphNode2.get_level()); 

	
	
