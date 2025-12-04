export const posts = [
  {
    id: 'getting-started-with-react-19',
    title: 'Getting Started with React 19',
    excerpt: 'Explore the new features in React 19, including the new Hook system improvements and compiler optimizations.',
    date: 'October 15, 2024',
    readTime: '5 min read',
    category: 'Development',
    image: 'https://via.placeholder.com/800x400',
    content: `
      <p>React 19 brings a host of new features that make building user interfaces easier and more efficient. In this post, we'll dive into the key updates.</p>
      
      <h3>The React Compiler</h3>
      <p>One of the most exciting additions is the automatic memoization provided by the React Compiler. This means less manual <code>useMemo</code> and <code>useCallback</code>.</p>

      <h3>Server Components by Default?</h3>
      <p>While not strictly "by default" for everything, the integration of Server Components is becoming more seamless...</p>
      
      <p>Stay tuned for more in-depth examples!</p>
    `
  },
  {
    id: 'mastering-tailwind-css',
    title: 'Mastering Tailwind CSS for Scalable UIs',
    excerpt: 'Tips and tricks for organizing your Tailwind classes and keeping your HTML clean in large projects.',
    date: 'November 2, 2024',
    readTime: '7 min read',
    category: 'Design',
    image: 'https://via.placeholder.com/800x400',
    content: `
      <p>Tailwind CSS is a utility-first framework that can speed up development significantly. However, without discipline, your classes can get out of hand.</p>
      
      <h3>Using @apply</h3>
      <p>Learn when to use the <code>@apply</code> directive to abstract common patterns into CSS classes.</p>

      <h3>Component Abstraction</h3>
      <p>The best way to clean up your HTML is to abstract repeated UI elements into reusable React components.</p>
    `
  },
  {
    id: 'future-of-web-development',
    title: 'The Future of Web Development: AI Integration',
    excerpt: 'How AI tools are changing the workflow of developers and what it means for the future of the industry.',
    date: 'December 1, 2024',
    readTime: '6 min read',
    category: 'Career',
    image: 'https://via.placeholder.com/800x400',
    content: `
      <p>Artificial Intelligence is no longer just a buzzword; it's a part of our daily dev workflow. From GitHub Copilot to ChatGPT, let's discuss the impact.</p>
      
      <h3>Productivity Boost</h3>
      <p>AI helps generate boilerplate code, write tests, and even debug complex issues.</p>
    `
  }
];
