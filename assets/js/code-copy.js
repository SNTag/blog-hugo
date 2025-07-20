document.addEventListener('DOMContentLoaded', function() {
  // Add copy buttons to all code blocks
  const codeBlocks = document.querySelectorAll('.highlight');
  
  codeBlocks.forEach(function(block) {
    const button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = 'Copy';
    button.addEventListener('click', function() {
      const code = block.querySelector('code');
      const text = code.textContent || code.innerText;
      
      navigator.clipboard.writeText(text).then(function() {
        button.textContent = 'Copied!';
        setTimeout(function() {
          button.textContent = 'Copy';
        }, 2000);
      }).catch(function(err) {
        console.error('Failed to copy: ', err);
        button.textContent = 'Error';
        setTimeout(function() {
          button.textContent = 'Copy';
        }, 2000);
      });
    });
    
    block.appendChild(button);
  });
});
