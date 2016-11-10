# Reasons for adopting DataJoint
If you are in a neuroscience lab that is transitioning from relatively simple and low-volume recordings to large-scale high-throughput and multimodal recordings and analysis, your current data management strategy probably comprises a collection of file folders with raw data recordings, spreadsheets with notes describing these data, analysis scripts that access these data (likely in MATLAB, Python, R, and Excel), saved intermediate results, and analysis output in the form of plots, tables, etc.
You probably have a set of naming conventions for files and folders to keep things organized.

If this describes your current situation, then adopting DataJoint will produce a number of advantages.
Most of them derive from the use of a database server (MySQL-compatible servers) rather than a simple file system.
But DataJoint adds several unique advantages as well.

## A uniform data model
DataJoint organizes all types of data using the exact same approach: the \emph{relational data model}.
Simply put, all data are stored as simple tables that are not nested within each other and are accessed directly rather than by following links between nodes.
Accessing all sorts of data requires no specialized readers or parsers.
There is no separation between acquired data and annotation (sometimes referred to as *metadata*).
Data definition, entry, computation, and query are performed using native constructs MATLAB and Python (two of the most commonly used languages for neural data analysis).

## Explicit data dependencies
When data are computed from other source data, any corrections made in the source data or in the processing routines require recomputing the dependent data.
DataJoint explicitly specifies, communicates, and enforces data dependencies between original and derived data, recursively.
The data dependencies define the sequence of the data processing chain and ensure data integrity all along the way.

## Fast, flexible access
The relational data model allows forming specific queries that retrieve only the required data.
DataJoint implements and streamlined and simplified query language to form data queries.
The stored data are indexed so that searches and manipulations are performed much faster than from data in distributed files.

## Uniform method for computing
DataJoint prescribes a uniform way for computing new data from existing data.
New computations are organized as distinct nodes following the same template.
Developers can understand each other's work more readily.

## Data sharing
The database server can provide access to multiple users within the same organization or across the Internet.

## Concurrent multiuser access
The database server allows simultaneous access to the same data to multiple users without corrupting the data or blocking each other.
DataJoint takes advantage of MySQL's transaction mechanisms to prevent users from seeing each other's incomplete results or overriding each other's work.

## Fine access control
Administrators of the database can grant or revoke specific types of access to specific subsets of data to specific users according to their roles in the projects and access privileges.

## Distributed processing and cloud computing
DataJoint implements its own internal job management system for distributed computing so that computations launched on multiple computers automatically coordinate their work and complete the jobs efficiently.
This simplifies migrating computation to cloud computing on platforms such as Amazon Web Services.