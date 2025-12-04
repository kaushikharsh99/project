export const posts = [
  {
    id: 'intro-to-transformers',
    title: 'Demystifying the Transformer Architecture',
    excerpt: 'A deep dive into the "Attention Is All You Need" paper and how Transformers revolutionized NLP.',
    date: 'October 15, 2024',
    readTime: '10 min read',
    category: 'Deep Learning',
    image: 'https://via.placeholder.com/800x400',
    content: `
      <p>The Transformer architecture has become the backbone of modern Natural Language Processing. In this post, we break down the Self-Attention mechanism.</p>
      
      <h3>The Encoder-Decoder Structure</h3>
      <p>Unlike RNNs, Transformers process the entire input sequence in parallel...</p>

      <h3>Multi-Head Attention</h3>
      <p>This allows the model to jointly attend to information from different representation subspaces at different positions.</p>
    `
  },
  {
    id: 'rag-vs-finetuning',
    title: 'RAG vs. Fine-Tuning: Which Strategy to Choose?',
    excerpt: 'Comparing Retrieval-Augmented Generation and Fine-Tuning for adapting LLMs to your specific domain data.',
    date: 'November 2, 2024',
    readTime: '8 min read',
    category: 'LLMs',
    image: 'https://via.placeholder.com/800x400',
    content: `
      <p>When customizing Large Language Models, developers often face a choice: should I fine-tune a model or use RAG? The answer depends on your data volatility and accuracy requirements.</p>
      
      <h3>Retrieval-Augmented Generation (RAG)</h3>
      <p>RAG is perfect when you need your model to access up-to-date information without retraining.</p>

      <h3>Fine-Tuning</h3>
      <p>Fine-tuning is better when you need to teach the model a specific style, format, or niche reasoning capability.</p>
    `
  },
  {
    id: 'data-cleaning-pandas',
    title: 'Advanced Data Cleaning with Pandas',
    excerpt: 'Practical techniques for handling missing values, outliers, and messy datasets in Python.',
    date: 'December 1, 2024',
    readTime: '6 min read',
    category: 'Data Science',
    image: 'https://via.placeholder.com/800x400',
    content: `
      <p>Data cleaning is 80% of a Data Scientist's job. Here are some advanced Pandas tricks to make it less painful.</p>
      
      <h3>Handling Missing Data</h3>
      <p>Beyond simple dropping, we explore imputation techniques like KNN Imputation.</p>
    `
  }
];