# Frontend Integration Guide

## Quick Start for Your Teammate

### API Base URL
```
Development: http://localhost:8000
Production: https://your-domain.com/api
```

## Main Endpoint: Protect Image

### Request
```javascript
POST /protect-image
Content-Type: multipart/form-data

Body:
- file: image file (required)
- user_id: string (optional)
```

### Response
- **Success (200)**: Returns protected image as PNG file
- **Error (400)**: Invalid file or too large
- **Error (429)**: Rate limited
- **Error (500)**: Processing failed

### Response Headers
```javascript
{
  "X-Protection-Level": "HIGH|MEDIUM|LOW",
  "X-Processing-Time": "1234.56",  // milliseconds
  "X-Image-ID": "abc123..."
}
```

## Frontend Implementation Examples

### React Example

```javascript
import React, { useState } from 'react';

function ImageProtector() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [protectedImage, setProtectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metadata, setMetadata] = useState(null);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const protectImage = async () => {
    if (!selectedFile) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('user_id', 'user123'); // Optional

    try {
      const response = await fetch('http://localhost:8000/protect-image', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        // Get metadata from headers
        setMetadata({
          protectionLevel: response.headers.get('X-Protection-Level'),
          processingTime: response.headers.get('X-Processing-Time'),
          imageId: response.headers.get('X-Image-ID')
        });

        // Get image blob
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        setProtectedImage(imageUrl);
      } else {
        alert('Failed to protect image');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Network error');
    } finally {
      setLoading(false);
    }
  };

  const downloadProtected = () => {
    const link = document.createElement('a');
    link.href = protectedImage;
    link.download = `protected_${selectedFile.name}`;
    link.click();
  };

  return (
    <div>
      <h1>Consentra Image Protection</h1>
      
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleFileSelect}
      />
      
      <button 
        onClick={protectImage} 
        disabled={!selectedFile || loading}
      >
        {loading ? 'Protecting...' : 'Protect Image'}
      </button>

      {protectedImage && (
        <div>
          <h2>Protected Image</h2>
          <img src={protectedImage} alt="Protected" style={{maxWidth: '100%'}} />
          
          {metadata && (
            <div>
              <p>Protection Level: {metadata.protectionLevel}</p>
              <p>Processing Time: {metadata.processingTime}ms</p>
            </div>
          )}
          
          <button onClick={downloadProtected}>
            Download Protected Image
          </button>
        </div>
      )}
    </div>
  );
}

export default ImageProtector;
```

### Vanilla JavaScript Example

```javascript
// Upload and protect image
async function protectImage(fileInput) {
  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', 'user123');

  try {
    const response = await fetch('http://localhost:8000/protect-image', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      // Get metadata
      const protectionLevel = response.headers.get('X-Protection-Level');
      const processingTime = response.headers.get('X-Processing-Time');
      
      console.log(`Protected with ${protectionLevel} level in ${processingTime}ms`);

      // Get image
      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      
      // Display
      document.getElementById('result').src = imageUrl;
      
      // Enable download
      document.getElementById('download').href = imageUrl;
      document.getElementById('download').download = `protected_${file.name}`;
    } else {
      const error = await response.text();
      alert(`Error: ${error}`);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Network error');
  }
}

// HTML
/*
<input type="file" id="fileInput" accept="image/*" onchange="protectImage(this)">
<img id="result" style="max-width: 100%;">
<a id="download" style="display: none;">Download Protected Image</a>
*/
```

### Vue.js Example

```vue
<template>
  <div class="image-protector">
    <h1>Protect Your Image</h1>
    
    <input 
      type="file" 
      @change="handleFileSelect"
      accept="image/*"
    />
    
    <button 
      @click="protectImage"
      :disabled="!selectedFile || loading"
    >
      {{ loading ? 'Protecting...' : 'Protect Image' }}
    </button>

    <div v-if="protectedImage" class="result">
      <h2>Protected Image</h2>
      <img :src="protectedImage" alt="Protected">
      
      <div v-if="metadata" class="metadata">
        <p>Protection Level: {{ metadata.protectionLevel }}</p>
        <p>Processing Time: {{ metadata.processingTime }}ms</p>
      </div>
      
      <button @click="downloadProtected">Download</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      protectedImage: null,
      metadata: null,
      loading: false
    };
  },
  methods: {
    handleFileSelect(event) {
      this.selectedFile = event.target.files[0];
    },
    
    async protectImage() {
      if (!this.selectedFile) return;
      
      this.loading = true;
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      formData.append('user_id', 'user123');

      try {
        const response = await fetch('http://localhost:8000/protect-image', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          this.metadata = {
            protectionLevel: response.headers.get('X-Protection-Level'),
            processingTime: response.headers.get('X-Processing-Time'),
            imageId: response.headers.get('X-Image-ID')
          };

          const blob = await response.blob();
          this.protectedImage = URL.createObjectURL(blob);
        } else {
          alert('Failed to protect image');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Network error');
      } finally {
        this.loading = false;
      }
    },
    
    downloadProtected() {
      const link = document.createElement('a');
      link.href = this.protectedImage;
      link.download = `protected_${this.selectedFile.name}`;
      link.click();
    }
  }
};
</script>
```

## Error Handling

```javascript
async function protectImage(file) {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:8000/protect-image', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      // Handle different error codes
      switch (response.status) {
        case 400:
          throw new Error('Invalid file or file too large (max 10MB)');
        case 429:
          throw new Error('Too many requests. Please wait a moment.');
        case 500:
          throw new Error('Server error. Please try again.');
        default:
          throw new Error('Unknown error occurred');
      }
    }

    return await response.blob();
  } catch (error) {
    console.error('Protection error:', error);
    throw error;
  }
}
```

## Loading States

```javascript
// Show progress during upload
function protectImageWithProgress(file, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    
    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percentage = (e.loaded / e.total) * 100;
        onProgress(percentage);
      }
    });
    
    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        resolve(xhr.response);
      } else {
        reject(new Error('Protection failed'));
      }
    });
    
    xhr.responseType = 'blob';
    const formData = new FormData();
    formData.append('file', file);
    
    xhr.open('POST', 'http://localhost:8000/protect-image');
    xhr.send(formData);
  });
}

// Usage
protectImageWithProgress(file, (progress) => {
  console.log(`Upload progress: ${progress}%`);
});
```

## Verify Watermark Endpoint

```javascript
async function verifyWatermark(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch('http://localhost:8000/verify-watermark', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  
  if (result.watermarked) {
    console.log('This image is protected!');
    console.log('Owner ID:', result.metadata.owner_id);
    console.log('Timestamp:', result.metadata.timestamp);
    return true;
  } else {
    console.log('No watermark found');
    return false;
  }
}
```

## Complete Workflow Example

```javascript
class ConsentraClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async protectImage(file, userId = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (userId) formData.append('user_id', userId);

    const response = await fetch(`${this.baseUrl}/protect-image`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Protection failed: ${response.statusText}`);
    }

    return {
      blob: await response.blob(),
      metadata: {
        protectionLevel: response.headers.get('X-Protection-Level'),
        processingTime: response.headers.get('X-Processing-Time'),
        imageId: response.headers.get('X-Image-ID')
      }
    };
  }

  async verifyWatermark(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/verify-watermark`, {
      method: 'POST',
      body: formData
    });

    return await response.json();
  }

  async getAnalytics() {
    const response = await fetch(`${this.baseUrl}/analytics`);
    return await response.json();
  }
}

// Usage
const client = new ConsentraClient();

// Protect image
const result = await client.protectImage(fileInput.files[0], 'user123');
console.log('Protected with', result.metadata.protectionLevel);

// Download protected image
const url = URL.createObjectURL(result.blob);
const link = document.createElement('a');
link.href = url;
link.download = 'protected_image.png';
link.click();
```

## UI/UX Tips for Hackathon Demo

### 1. Show Protection Level
```javascript
const levelColors = {
  'HIGH': '#ef4444',    // Red
  'MEDIUM': '#f59e0b',  // Orange
  'LOW': '#10b981'      // Green
};

const levelIcons = {
  'HIGH': '🔒',
  'MEDIUM': '🛡️',
  'LOW': '✓'
};
```

### 2. Show Processing Time
```javascript
<div class="stats">
  <span>Protected in {processingTime}ms</span>
  <span>{protectionLevel} protection applied</span>
</div>
```

### 3. Before/After Comparison
```javascript
<div class="comparison">
  <div>
    <h3>Original</h3>
    <img src={originalImage} />
  </div>
  <div>
    <h3>Protected</h3>
    <img src={protectedImage} />
    <p>Visually identical, AI-resistant</p>
  </div>
</div>
```

### 4. Analytics Dashboard
```javascript
const analytics = await client.getAnalytics();

<div class="dashboard">
  <div>Total Protected: {analytics.total_processed}</div>
  <div>Avg Time: {analytics.avg_processing_time_ms}ms</div>
  <div>
    High: {analytics.protection_levels.HIGH}
    Medium: {analytics.protection_levels.MEDIUM}
    Low: {analytics.protection_levels.LOW}
  </div>
</div>
```

## Testing Checklist

- [ ] Upload image (PNG, JPG)
- [ ] See loading state
- [ ] Receive protected image
- [ ] Display protection level
- [ ] Download protected image
- [ ] Verify watermark
- [ ] Handle errors gracefully
- [ ] Show rate limiting message
- [ ] Mobile responsive
- [ ] File size validation

## Common Issues

### CORS Error
If you see CORS errors, make sure the backend CORS is configured:
```python
# In backend main.py
allow_origins=["http://localhost:3000"]  # Your frontend URL
```

### File Too Large
Max size is 10MB. Show error:
```javascript
if (file.size > 10 * 1024 * 1024) {
  alert('File too large! Max 10MB');
  return;
}
```

### Rate Limiting
Handle 429 status code:
```javascript
if (response.status === 429) {
  alert('Too many requests. Please wait a minute.');
}
```

## Demo Script for Hackathon

1. **Upload a selfie** → Should get HIGH protection
2. **Upload a landscape** → Should get LOW protection
3. **Show processing time** → ~1-3 seconds
4. **Download protected image** → Looks identical to original
5. **Verify watermark** → Shows owner ID and timestamp
6. **Show analytics** → Display processing stats

---

Need help? Check the API docs at: `http://localhost:8000/docs`
