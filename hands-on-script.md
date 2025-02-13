# Case Study Presentation Notes

## Introduction
- Brief overview of the task: Design a data catalog system for exploring technical and business metadata
- Highlight the key requirements: 10+ schemas, business context, metadata presentation

## The Data Model
The sample data represents a fictitious real estate company that provides property listings and 
valuation services for buyers.

The system contains the following key schemas:

1. **real_estate_listings**: Core property listing data, photos, and location information
2. **sales**: Customer and transaction management
3. **marketing**: SEO, social media campaigns, and engagement tracking
4. **user_behaviour**: Website analytics and email engagement
5. **customer_support**: Support tickets and customer interactions
6. **real_estate_trackers**: Property search preferences and notifications
7. **czech_market_data**: Regional market statistics and trends
8. **location_amenities**: Nearby facilities and transport information
9. **human_resources**: Internal team management
10. **cloud_infrastructure**: System operations and costs

## Solution Approach
- Why OpenMetadata was chosen:
  * Production-ready, enterprise-grade solution
  * Rich metadata management capabilities out of the box
  * REST API for automation and extensibility
  * UI for metadata exploration
  * Support for both technical and business metadata

## Demo
- Show the running system:
  * OpenMetadata UI navigation
  * Schema exploration
  * Business metadata visibility
  * Search functionality
  * User roles and permissions

## Future Enhancements
- Data quality metrics integration
- Automated business metadata collection
- Data lineage tracking
- Integration with data governance tools
- API extensions for custom functionality
