def largestRectHist(heights):
	stack = [-1];
	maxArea = 0;

	for i in range(len(heights)):
		# keep poping out of the stack till the stack is empty
		# or till  top of stack is greater than next height
		while stack[-1] != -1 and heights[stack[-1]] >= heights[i]:
			lastElementIndex = stack.pop()
			maxArea = max(maxArea, heights[lastElementIndex] * (i - stack[-1] -1)) 

		stack.append(i)

	while stack[-1] != -1:
		lastElementIndex = stack.pop()
		maxArea = max(maxArea, heights[lastElementIndex] * (len(heights) - stack[-1] -1)) 
	return maxArea

print largestRectHist([1,2,3,0,2,3,4])




