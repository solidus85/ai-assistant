/**
 * Work Assistant module for managing projects, emails, and status updates
 */

import { apiCall } from './api.js';

class WorkAssistant {
    constructor() {
        this.currentProject = null;
        this.projects = [];
        this.deliverables = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadProjects();
        this.loadUpcomingDeliverables();
    }

    setupEventListeners() {
        // Project management
        const addProjectBtn = document.getElementById('add-project-btn');
        if (addProjectBtn) {
            addProjectBtn.addEventListener('click', () => this.showAddProjectDialog());
        }

        // Email processing
        const processEmailBtn = document.getElementById('process-email-btn');
        if (processEmailBtn) {
            processEmailBtn.addEventListener('click', () => this.showProcessEmailDialog());
        }

        // Status updates
        const addStatusBtn = document.getElementById('add-status-btn');
        if (addStatusBtn) {
            addStatusBtn.addEventListener('click', () => this.showAddStatusDialog());
        }

        // Deliverables
        const addDeliverableBtn = document.getElementById('add-deliverable-btn');
        if (addDeliverableBtn) {
            addDeliverableBtn.addEventListener('click', () => this.showAddDeliverableDialog());
        }

        // Query
        const queryBtn = document.getElementById('work-query-btn');
        const queryInput = document.getElementById('work-query-input');
        if (queryBtn && queryInput) {
            queryBtn.addEventListener('click', () => this.processQuery());
            queryInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.processQuery();
                }
            });
        }
    }

    async loadProjects() {
        try {
            const response = await apiCall('/api/work/projects', 'GET');
            this.projects = response;
            this.renderProjects();
        } catch (error) {
            console.error('Failed to load projects:', error);
        }
    }

    renderProjects() {
        const projectsList = document.getElementById('projects-list');
        if (!projectsList) return;

        projectsList.innerHTML = '';
        
        this.projects.forEach(project => {
            const projectItem = document.createElement('div');
            projectItem.className = 'project-item';
            projectItem.innerHTML = `
                <div class="project-name">${project.name}</div>
                <div class="project-company">${project.company || ''}</div>
            `;
            projectItem.addEventListener('click', () => this.selectProject(project));
            projectsList.appendChild(projectItem);
        });
    }

    selectProject(project) {
        this.currentProject = project;
        
        // Update UI to show selected project
        document.querySelectorAll('.project-item').forEach(item => {
            item.classList.remove('selected');
        });
        event.currentTarget.classList.add('selected');
        
        // Load project-specific data
        this.loadProjectData(project.id);
    }

    async loadProjectData(projectId) {
        try {
            // Load emails for project
            const emails = await apiCall(`/api/work/emails?project_id=${projectId}`, 'GET');
            
            // Load status updates
            const statusUpdates = await apiCall(`/api/work/status-updates/${projectId}`, 'GET');
            
            // Display in output area
            this.displayProjectInfo(emails, statusUpdates);
        } catch (error) {
            console.error('Failed to load project data:', error);
        }
    }

    displayProjectInfo(emails, statusUpdates) {
        const output = document.getElementById('work-output');
        if (!output) return;

        let html = `<h3>${this.currentProject.name}</h3>`;
        
        if (statusUpdates && statusUpdates.length > 0) {
            html += '<h4>Recent Status Updates</h4>';
            statusUpdates.slice(0, 3).forEach(update => {
                html += `
                    <div class="status-update">
                        <div class="update-date">${new Date(update.created_at).toLocaleDateString()}</div>
                        <div class="update-content">${update.content}</div>
                    </div>
                `;
            });
        }
        
        if (emails && emails.length > 0) {
            html += '<h4>Recent Emails</h4>';
            emails.slice(0, 3).forEach(email => {
                html += `
                    <div class="email-item">
                        <div class="email-subject">${email.subject}</div>
                        <div class="email-from">From: ${email.sender}</div>
                        <div class="email-date">${new Date(email.received_date).toLocaleDateString()}</div>
                    </div>
                `;
            });
        }
        
        output.innerHTML = html;
    }

    async loadUpcomingDeliverables() {
        try {
            const response = await apiCall('/api/work/deliverables?upcoming_days=7', 'GET');
            this.deliverables = response;
            this.renderDeliverables();
        } catch (error) {
            console.error('Failed to load deliverables:', error);
        }
    }

    renderDeliverables() {
        const deliverablesList = document.getElementById('deliverables-list');
        if (!deliverablesList) return;

        deliverablesList.innerHTML = '';
        
        if (this.deliverables.length === 0) {
            deliverablesList.innerHTML = '<p class="no-items">No upcoming deliverables</p>';
            return;
        }
        
        this.deliverables.forEach(deliverable => {
            const item = document.createElement('div');
            item.className = `deliverable-item priority-${deliverable.priority}`;
            
            const dueDate = new Date(deliverable.due_date);
            const daysUntil = Math.ceil((dueDate - new Date()) / (1000 * 60 * 60 * 24));
            
            item.innerHTML = `
                <div class="deliverable-title">${deliverable.title}</div>
                <div class="deliverable-project">${deliverable.project_name}</div>
                <div class="deliverable-due">Due in ${daysUntil} days</div>
            `;
            deliverablesList.appendChild(item);
        });
    }

    showAddProjectDialog() {
        const name = prompt('Project Name:');
        if (!name) return;
        
        const company = prompt('Company (optional):');
        const description = prompt('Description (optional):');
        
        this.createProject({ name, company, description });
    }

    async createProject(projectData) {
        try {
            const response = await apiCall('/api/work/projects', 'POST', projectData);
            this.projects.push(response);
            this.renderProjects();
            this.showMessage('Project created successfully');
        } catch (error) {
            console.error('Failed to create project:', error);
            this.showMessage('Failed to create project', 'error');
        }
    }

    showProcessEmailDialog() {
        const dialog = document.createElement('div');
        dialog.className = 'modal-dialog';
        dialog.innerHTML = `
            <div class="modal-content">
                <h3>Process Email</h3>
                <input type="text" id="email-subject" placeholder="Subject" />
                <input type="text" id="email-sender" placeholder="From (email address)" />
                <textarea id="email-content" placeholder="Paste email content here..." rows="10"></textarea>
                <div class="modal-buttons">
                    <button onclick="workAssistant.processEmail()">Process</button>
                    <button onclick="this.closest('.modal-dialog').remove()">Cancel</button>
                </div>
            </div>
        `;
        document.body.appendChild(dialog);
    }

    async processEmail() {
        const subject = document.getElementById('email-subject').value;
        const sender = document.getElementById('email-sender').value;
        const content = document.getElementById('email-content').value;
        
        if (!content) {
            alert('Please provide email content');
            return;
        }
        
        try {
            const response = await apiCall('/api/work/emails/process', 'POST', {
                subject,
                sender,
                content,
                recipients: [],
                received_date: new Date().toISOString()
            });
            
            document.querySelector('.modal-dialog').remove();
            
            // Display results
            const output = document.getElementById('work-output');
            output.innerHTML = `
                <h3>Email Processed</h3>
                <div class="processed-info">
                    <p><strong>Project:</strong> ${response.extracted_info.project_name || 'Not identified'}</p>
                    <p><strong>Company:</strong> ${response.extracted_info.company || 'Not identified'}</p>
                    <p><strong>People:</strong> ${response.extracted_info.people?.join(', ') || 'None'}</p>
                    <p><strong>Keywords:</strong> ${response.extracted_info.keywords?.join(', ') || 'None'}</p>
                    <p><strong>Importance:</strong> ${response.extracted_info.importance}</p>
                    <p><strong>Summary:</strong> ${response.extracted_info.summary}</p>
                </div>
            `;
            
            // Reload projects if new one was created
            if (response.project) {
                this.loadProjects();
            }
            
        } catch (error) {
            console.error('Failed to process email:', error);
            this.showMessage('Failed to process email', 'error');
        }
    }

    showAddStatusDialog() {
        if (!this.currentProject) {
            alert('Please select a project first');
            return;
        }
        
        const content = prompt(`Add status update for ${this.currentProject.name}:`);
        if (!content) return;
        
        this.addStatusUpdate(content);
    }

    async addStatusUpdate(content) {
        try {
            const response = await apiCall('/api/work/status-updates', 'POST', {
                project_id: this.currentProject.id,
                content,
                created_by: 'User'
            });
            
            this.showMessage('Status update added successfully');
            
            // Reload project data
            this.loadProjectData(this.currentProject.id);
            
        } catch (error) {
            console.error('Failed to add status update:', error);
            this.showMessage('Failed to add status update', 'error');
        }
    }

    showAddDeliverableDialog() {
        if (!this.currentProject) {
            alert('Please select a project first');
            return;
        }
        
        const title = prompt('Deliverable title:');
        if (!title) return;
        
        const dueDate = prompt('Due date (YYYY-MM-DD):');
        const priority = prompt('Priority (low/medium/high):', 'medium');
        
        this.addDeliverable({ title, due_date: dueDate, priority });
    }

    async addDeliverable(deliverableData) {
        try {
            const response = await apiCall('/api/work/deliverables', 'POST', {
                ...deliverableData,
                project_id: this.currentProject.id
            });
            
            this.showMessage('Deliverable added successfully');
            this.loadUpcomingDeliverables();
            
        } catch (error) {
            console.error('Failed to add deliverable:', error);
            this.showMessage('Failed to add deliverable', 'error');
        }
    }

    async processQuery() {
        const queryInput = document.getElementById('work-query-input');
        const query = queryInput.value.trim();
        
        if (!query) return;
        
        const output = document.getElementById('work-output');
        output.innerHTML = '<p>Processing query...</p>';
        
        try {
            const response = await apiCall('/api/work/query', 'POST', { query });
            
            let html = `
                <div class="query-response">
                    <h4>Query: ${query}</h4>
                    <div class="answer">${response.answer}</div>
            `;
            
            // Display deliverables if found
            if (response.results.deliverables && response.results.deliverables.length > 0) {
                html += '<h5>Deliverables:</h5>';
                response.results.deliverables.forEach(d => {
                    html += `
                        <div class="result-item">
                            <strong>${d.title}</strong> - ${d.project_name}
                            <br>Due: ${new Date(d.due_date).toLocaleDateString()}
                            <br>Status: ${d.status}
                        </div>
                    `;
                });
            }
            
            // Display emails if found
            if (response.results.emails && response.results.emails.length > 0) {
                html += '<h5>Related Emails:</h5>';
                response.results.emails.forEach(e => {
                    html += `
                        <div class="result-item">
                            <strong>${e.metadata.subject}</strong>
                            <br>From: ${e.metadata.sender}
                            <br>Relevance: ${Math.round(e.similarity_score * 100)}%
                        </div>
                    `;
                });
            }
            
            // Display status updates if found
            if (response.results.status_updates && response.results.status_updates.length > 0) {
                html += '<h5>Status Updates:</h5>';
                response.results.status_updates.forEach(s => {
                    html += `
                        <div class="result-item">
                            ${s.content.substring(0, 200)}...
                            <br>Project: ${s.metadata.project_name}
                            <br>Relevance: ${Math.round(s.similarity_score * 100)}%
                        </div>
                    `;
                });
            }
            
            html += '</div>';
            output.innerHTML = html;
            
            // Clear input
            queryInput.value = '';
            
        } catch (error) {
            console.error('Failed to process query:', error);
            output.innerHTML = '<p class="error">Failed to process query</p>';
        }
    }

    showMessage(message, type = 'success') {
        const output = document.getElementById('work-output');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        output.prepend(messageDiv);
        
        setTimeout(() => messageDiv.remove(), 3000);
    }
}

// Create and export instance
const workAssistant = new WorkAssistant();
export { workAssistant };

// Make available globally for inline handlers
window.workAssistant = workAssistant;