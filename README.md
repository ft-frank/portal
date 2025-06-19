# PortalHSC
A student portal designed for tutoring centres.



## Idenifying and Defining 


### Define and analyse problem requirements
The following tables outlines both functional and performance requirements, prioritized from most essential to optional, distinguishing between core needs and potential opportunities for future implementation.

#### Needs 
| Feature                  | Functional Requirement  | Performance Requirement |
|--------------------------|------------------------ |--------------------------|
| Login Functionality      | The system will include a user authentication feaure that verifies user credentials before granting access to eprsonalised content| Login requets must be processed within 2 seconds under normal load |
| Homework Submission      | Students must be able to submit homework assignments directly through the portal.        | Uploads must support common file types (PDF, DOCX, JPG) with confirmation within 2 seconds.  |
| Homework Feedback        | Tutors must be able to return marked homework with comments and grades.                               | Feedback must be accessible within 2 seconds of release, with optional download.             |
| Class Timetable & Details| Students should be able to view upcoming classes, times, subjects, and tutor information.             | Updates to schedules must reflect in real-time with minimal latency.                         |
| Invoice & Payment Viewing| Parents/students must be able to access current and past invoices.                                    | Invoices must load within 1–2 seconds and be available for PDF export.                       |
| Solution Access          | Students should be able to access worked solutions or model answers.                                  | Should be available offline after first access and optimized for mobile viewing.             |
| Student Profile Overview | Tutors/admins must be able to view student progress, class history, and notes.                        | Access must be secure, authenticated, and responsive under load.                             |
| Announcement System      | Enable tutors/admins to broadcast messages and updates.| Must not interfere with performance and should be optimized for mobile devices.              |

#### Oppurtunities
| Feature                | Functional Requirement| Performance Requirement|
|------------------------|-----------------------|------------------------|
| Question Bank          | Provide a categorized database of practice problems and exam questions.     | Searchable by subject, difficulty, and topic with fast filtering.              |
| Gamification Elements  | Introduce badges or progress rewards to motivate students.                  | Must not interfere with performance and should be optimized for mobile devices. |


### Scheduling and financial feasibility

Following comprehensive discussions with the client, the client HopeHSC requres a digital solution designed to streamline academic and adminstrative interactions between students and tutors. Therefore they have contacted us, the Fort Street Software Solutions Company, to create a tool that assists these students in preparation for the HSC. This tool will be a progressive web application (PWA) that increases efficiency of tasks such as marking homeworking, and managing invoices through digitisation. The name for this project will be "PortalHSC"

Functionality Requirements: 
- Login Functionality for students and teachers to have accounts.
- Allow students to submit homework online.
- Enable tutors to provide feedback on submitted homework.
- Display class schedules and details to students.
- Show invoices and payment history.
- Provide access to homework solutions.
- Allow tutors/admins to view student profiles and progress.
- Send announcements to users.
- (Optional) Offer a searchable question bank.
- (Optional) Include gamification features like badges.

Performance Requirements: 
- All core features must be fully functional offline.
- Maintain responsive performance and avoid lag
- Interoperability between devices of different manufacturers
- Avaliable through variety of internet browsers.
- All data retrieval and submission must be secure and reliable under varying network conditions.

All <ins>needs</ins> listed within the functional requirements will be completed before the optional <ins>oppurtunities</ins>. Prioritising these ensurs that the core user requirements are met, enabling basic tutoring and adminstrative processes, therefore suceeding in providing a solution for HopeHSC. The oppurtunities will be addressed later, as they enhance user experience but are not critical for the intial operation of the system. 
All functionalities are independant of each other, except the interaction betwen allowing homeworks to submit homework online, and enabling tutors to provide feedback on this submitted homework. 

Costs include: 
- Development costs: Time and effort invested in designing, coding, testing and deploying the PWA. 
- Hosting and Infrastructure: There may be a possibility of fees for cloud services or servers needed to host the application and store data securely

#### Entities, Data Structures, and Data Types

- Student
  - Data Structure: Array of records or database table
  - Data Types:
    - `String` – name, email
    - `Integer` – age, student ID
    - `Boolean` – active/inactive status

- Tutor
  - Data Structure: Array of records or database table
  - Data Types:
    - `String` – name, subject area
    - `Integer` – tutor ID
    - `Array` – list of assigned class IDs

- Homework
  - Data Structure: Array of records or database table
  - Data Types:
    - `String` – title, feedback comments
    - `Date` – due date
    - `File` – uploaded homework file
    - `Integer` – mark awarded

- Invoice
  - Data Structure: Array of records or database table
  - Data Types:
    - `Integer` – amount
    - `Date` – issue date, due date
    - `Boolean` – payment status

- Class
  - Data Structure: Array of records or database table
  - Data Types:
    - `String` – subject, location
    - `Date` – date and time
    - `Integer` – duration in minutes
    - `Array` – list of enrolled student IDs

- Solution
  - Data Structure: Array of records or database table
  - Data Types:
    - `String` – solution text
    - `File` – attachment
    - `Integer` – related homework ID

- Announcement
  - Data Structure: Array of records
  - Data Types:
    - `String` – title, content
    - `Date` – time posted

- Question Bank
  - Data Structure: Nested array or separate database table
  - Data Types:
    - `String` – question text, topic
    - `Integer` – difficulty level
    - `Boolean` – whether answered

- Gamification Badge (optional)
  - Data Structure: Array stored within student record
  - Data Types:
    - `String` – badge name
    - `Date` – date earned

#### Boundaries

The tutoring portal PWA will operate within defined boundaries to ensure it remains manageable and be able to function its core purpose. Several aspects that fall under the services of HopeHSC will remain outside the system. These include:

- Live tutoring sessions, which will occur using external platforms such as Zoom.
- Payment processing for invoices will not be handled directly; instead the system will only display invoices. Payments options will be decided by HopeHSC, however will likely involve either bank transfer and cash payments in termly instalments.
- Authentication systems such as Google Oauth aren't necessary, as there is limited to no malicious activity possible and the userbase will be private. Accounts will be created as required by admins.
- Any policies, curriculum changes and rules will be agreed to and signed externally.

#### Tools
A description of a veriety of different tools used during the production and implemntation of the PWA. 

| Tool             | Description                                                  |
|------------------|--------------------------------------------------------------|
| Screenshot       |            |
| Description      |             |
| Algorithm Design |  |
| Brainstorming    |        |
| Code Generation  |                |
| Data Dictionaries|      |
| Debugging        |                       |
| Installation     |                |
| Maintenance      |               |
| Mind-Mapping     |                |
| Storyboards      |              |
| Testing          |  |

#### Software implementation methods. 

**Pilot** implementation involves rolling out the new system to a small, manageable group of users before a full-scale implementation. This method allows organisations to identify any issues or necessary adjustments in a controlled environment, reducing the risk of widespread problems.

A pilot implementation is beneficial as by letting the tutoring portal be tested by a small group first, they can help identify and fix issues without wasting other students' time potentially dealing with a flawed system. Once the group and developer are satisfied with the solutoin, then it may be distrubited amongst the student body as a complete package, either immediately replacing the old system or filling in the digital gap within HopeHSC. 

Direct implementatio would be risky, as the new system has not been thoroughly tested. 
Parallel implementation would confuse the administrative, student and teaching staff during operations. 
Phased implementation will take too long to implement. 

## Reserach and Planning
### Project Management
Project management is the process of planning, organizing, and overseeing tasks and resources to achieve specific project goals within a set timeframe and budget. It ensures that a project is completed efficiently, meets requirements, and delivers value to clients
#### Software Development Approaches

 <ins>The Waterfall Software Development Approach</ins>

| Question | Sample Explanation |
|----------|--------------------|
| 1.1 How are the logical progression of steps used throughout the life cycle? | The Waterfall model follows a strict, linear sequence of stages. Each stage must be fully completed before the next begins, ensuring a clear and logical flow. |
| 1.2 What are the stages of ‘falling water’? | Requirements Gathering<br>System Design<br>Implementation (Coding)<br>Testing<br>Deployment<br>Maintenance |
| 1.3 What are the advantages and disadvantages of this approach? | Advantages:<br>- Easy to manage due to its rigid structure<br>- Good for small or well-defined projects<br>- Documentation is thorough and complete<br>Disadvantages:<br>- Inflexible to changes<br>- No working product until late in the process<br>- Late discovery of issues during development can be costly |
| 1.4 Give examples of the scale and types of developments that use this approach. | - Large-scale government or defence systems (tax systems)<br>- Large construction and infrastructure (bridges, air traffic control)<br>- Large-scale manufacturing projects (cars, vehicles)<br>- Large-scale healthcare projects (medical-record systems, medicinal rollout) |

---

<ins>The WAgile Software Development Approach</ins>

| Question | Sample Explanation |
|----------|--------------------|
| 2.1 Explain why it is a hybrid model | WAgile is hybrid as it combines the structure of Waterfall (upfront planning, documentation, etc.) and Agile’s flexibility (e.g., iterations, user feedback). |
| 2.2 Analyse the ‘when’ intervention is applied during the development life cycle | Agile practices (like stand-ups, iterative development, testing) are introduced after the initial Waterfall stages, often during implementation or testing. It may start rigid but loosen control during later phases for adaptability. |
| 2.3 Analyse the ‘how’ intervention is applied during the development life cycle | Agile interventions are layered into Waterfall by:<br>- Splitting implementation into sprints<br>- Including regular stakeholder reviews<br>- Allowing feedback loops during testing<br>This hybridization enables flexibility while maintaining upfront planning. |
| 2.4 Give examples scale and types of developments that use this approach | - Medium to large projects in corporate environments<br>- Government or healthcare systems with compliance requirements<br>- Projects with fixed deadlines but evolving features |

---

<ins>The Agile Software Development Approach</ins>

| Question | Sample Explanation |
|----------|--------------------|
| 3.1 What is the rate of developing a final solution? | Agile delivers a working product early and often, typically every 1-4 weeks in sprints. |
| 3.2 Explain method tailoring | Method tailoring involves adapting Agile methods (like Scrum, Kanban) to suit the team or project. For example, adjusting sprint lengths, roles, or tools to match the team’s needs and the project scope. |
| 3.3 Explain iteration workflow | Each iteration (or sprint) concludes a round of:<br>- Planning<br>- Design<br>- Development<br>- Testing<br>- Review<br>After each cycle, feedback is incorporated into the next iteration, enabling rapid improvements. |
| 3.4 Give examples of the scale and types of developments that use this approach | - Web and mobile app startups<br>- SaaS platforms<br>- Games and creative media projects<br>- Generally all small to medium sized projects |

<ins>Venn Diagram</ins>

![image](https://github.com/user-attachments/assets/ff3aeb3c-fcdb-49a9-9ec9-7068c5b74aa8)

<ins>Development Approach</ins> 

A **Wagile** approach to development would be implemented for PortalHSC due to the its balance of structure, planning and flexibility in time-restrained projects. 

The WAgile development process is the most efficient choice for PortalHSC project, as it combines the structured planning of Waterfall with the flexibility of Agile. This hybrid model allows for clear documentation and requirement definition, which is ideal for meeting the client's standards (school project) whilst also supporting iterative devleopment and feedback during implemenation. WAgile ensures the project stays organised yet adaptable, making it well-sstuied for our solo developer team with fixed deadlines and evolving feature needs. 


#### Scheduling and Task allocation 
![image](https://github.com/user-attachments/assets/7050220e-63b3-439b-aca9-8f9b3474e8bd)

#### Collaboration Tools

| Tool           | Description                                                   | Screenshot                |
|----------------|---------------------------------------------------------------|---------------------------|
| Visual Studio Code | A lightweight code editor used for writing and managing source code. |  |
| GitHub             | A platform for version control and collaboration using Git.   |  |
| Flask              | A Python web framework used to develop the PWA backend.       |  |
| Chrome DevTools    | Browser tools for debugging and testing web applications.     | |
| Lucidchart         | A diagramming tool used to plan system architecture and workflows.     |
|

#### Social and Ethic aspects of software enginering projects

<ins>Privacy</ins>

Data required by the client from each student will involve:
-Student Name
-School
-Parent Email
-Student Email
-Parent Phone Number
-Student Mobile Number


Data required by the client from each tutor will involve:
- Tutor Name
- Tutor Email
- Tutor Mobile

Privacy is essential when handling student information such as names, emails, and homework submissions. All data will be stored securely and not shared with third parties. 

<ins>Security</ins>

The issue of security applies to the process of homework submissions and account login. To prevent common threats like cross-site scripting (XSS) and SQL injection, all inputs will be validated and sanitised. Addtionally, passwords will be hashed and HTTPS will be used to encrpt data in transit. Homework submission will also be limited to PDF. 


<ins>Accessibility and Inclusivity</ins>
Accesibility ensures all students can use the portal regardless of ability. THe UI will follow WCAG guidelines  by using proper colour contrast, alt test for imags, and keyboard navigation. 

<ins>Transparency</ins>
Transparency means users should know how the platform works and what it does with their data. A clear “How it works” section will explain features such as homework tracking, feedback systems, and how logins are handled.

<ins>Fairness</ins>

Fairness ensurs that our software does not discriminate against any group or individual. Featurs such as homework feedback, class details and resource access etc. must be equally avaliagle to all users regardless of their backgroud and avoid biases in its functionality.

<ins>Intellectual Property</ins>
The platform will respect intellectual property laws by using only open-source assets. Any third-party frameworks and libaries used(e.g. Bootstrap, Flask) will be  attributed and licensed. Tutors uploading content will agree not to upload copyrighted material without permission. 

<ins>Collaboration</ins>
Collaboration between the client, our developers and the clients' students is essential in building a successful solutoin. Regular feedback from tutors during development would help align features with real needs, such as homework return systems. 

<ins>Feedback</ins>
PortalHSC wil include a feedback form that allows students and tutors to report bugs or suggest improvements. This feedback will be reviewed reguarly, and the information gathered will be used to plan future updates. Feedback encourages a user-focused proces of development and ensurs the platform continutes to improve.





#### Quality Assurance

|Quality Criteria | Explanation                                                  |
|-----------------|--------------------------------------------------------------|
|Google Lighthouse|Google Lighthouse is an automated tool developed by Google that analyses web pages and generates a score from 0 to 100 based on various factors like performance, accessibility, best practices, SEO and PWA. An ideal score is anywhere from 90-100.|
|Response Timme   | The software should respond to all user requests in a time of less than 3 seconds|
|Interoperability |


| Quality Criteria         | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
|Google Lighthouse|Google Lighthouse is an automated tool developed by Google that analyses web pages and generates a score from 0 to 100 based on various factors like performance, accessibility, best practices, SEO and PWA. An ideal score is anywhere from 90-100.|
| Responsiveness           | The interface should work seamlessly on mobile, tablet, and desktop devices. |
| Accessibility Compliance | Meets WCAG 2.1 Level AA guidelines for accessibility.                      |
| Ease of Navigation       | Users can access any feature within 2–3 clicks from the homepage.          |
| Minimal Load Time        | Pages should load in under 2 seconds on a standard connection.             |

#### Compliace and Legislative Requirements

| Compliance or Legislative Issue                  | Methods for Mitigation                                                                 |
|--------------------------------------------------|----------------------------------------------------------------------------------------|
| Privacy Act 1988 (Cth)                           | Collect only necessary user data, display a clear privacy policy, obtain user consent before data collection, and ensure data is securely stored and not shared without permission. |
| Privacy and Personal Information Protection Act 1998 (NSW) | Implement access controls, limit data visibility to relevant users (e.g., tutors can only see their students), and encrypt sensitive information. |
| Spam Act 2003 (Cth)                              | Ensure that any communications (e.g., reminders or announcements) include consent and an option to opt out. |
| Copyright Act 1968 (Cth)                         | Use only licensed or original materials (e.g., icons, past paper content), and credit sources when required. |
| Australian Consumer Law                          | Provide accurate, non-misleading descriptions of the PWA's features, especially if a payment component (e.g., invoicing) is integrated. |
| ISO/IEC 27001 (Information Security Management)  | Follow industry best practices for information security: implement strong password rules, use HTTPS, and conduct regular security audits. |



#### System Modelling





