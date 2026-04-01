import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.services.models import Service, ServiceFAQ

# Update service details with comprehensive information
services_data = {
    'tax-health-checks': {
        'long_description': '''
        <h3>Tax Health Check Overview</h3>
        <p>A comprehensive tax compliance and health assessment that evaluates your current tax position and identifies optimization opportunities.</p>
        
        <h4>What We Do:</h4>
        <ul>
            <li>Review your historical tax returns and compliance status</li>
            <li>Analyze your tax filing obligations and deadlines</li>
            <li>Identify potential compliance gaps or risks</li>
            <li>Assess opportunities for legitimate tax optimization</li>
            <li>Provide recommendations for improved tax management</li>
        </ul>
        
        <h4>Who Needs This:</h4>
        <p>Ideal for businesses experiencing growth, changes in operations, or those unsure about their tax compliance position. Perfect for companies relocating to Kenya or expanding their operations.</p>
        
        <h4>Deliverables:</h4>
        <ul>
            <li>Comprehensive tax assessment report</li>
            <li>Compliance audit findings</li>
            <li>Risk analysis and mitigation recommendations</li>
            <li>Tax optimization roadmap</li>
        </ul>
        
        <h4>Benefits:</h4>
        <ul>
            <li>Reduce tax liabilities through legitimate optimization</li>
            <li>Ensure complete KRA compliance</li>
            <li>Avoid penalties and interest charges</li>
            <li>Make informed business decisions</li>
            <li>Plan for future tax obligations</li>
        </ul>
        '''
    },
    'strategic-tax-advisory': {
        'long_description': '''
        <h3>Strategic Tax Advisory Services</h3>
        <p>Expert tax planning and strategic advisory services designed to minimize your tax burden legally while supporting your business growth objectives.</p>
        
        <h4>Services Include:</h4>
        <ul>
            <li>Business structure optimization (Sole trader, Partnership, Company)</li>
            <li>Tax-efficient investment planning</li>
            <li>Year-end tax planning strategies</li>
            <li>Succession planning and tax implications</li>
            <li>International tax considerations</li>
        </ul>
        
        <h4>Strategic Areas:</h4>
        <ul>
            <li>Corporate restructuring planning</li>
            <li>Dividend optimization strategies</li>
            <li>Deduction maximization</li>
            <li>Loss utilization strategies</li>
            <li>Tax deferral opportunities</li>
        </ul>
        
        <h4>Client Outcomes:</h4>
        <ul>
            <li>Significant tax savings (often 10-30% for structured businesses)</li>
            <li>Improved cash flow management</li>
            <li>Reduced audit risk through compliant planning</li>
            <li>Better long-term financial planning</li>
            <li>Strategic business advantages</li>
        </ul>
        
        <h4>Process:</h4>
        <p>We begin with a comprehensive consultation to understand your business, goals, and financial situation. We then develop customized strategies, present options with their tax implications, and implement the optimal solution.</p>
        '''
    },
    'income-tax-filing-advisory': {
        'long_description': '''
        <h3>Income Tax Filing and Advisory</h3>
        <p>Professional income tax return preparation and personalized advisory services for both individuals and businesses.</p>
        
        <h4>For Individuals:</h4>
        <ul>
            <li>Employment income optimization</li>
            <li>Investment income reporting</li>
            <li>Relief claims and deductions</li>
            <li>Personal tax planning</li>
            <li>Non-resident taxation</li>
        </ul>
        
        <h4>For Businesses:</h4>
        <ul>
            <li>Comprehensive business income assessment</li>
            <li>Expense documentation and deduction optimization</li>
            <li>Capital allowance calculations</li>
            <li>Business structure tax treatment</li>
            <li>Estimated tax payments and planning</li>
        </ul>
        
        <h4>Services Provided:</h4>
        <ul>
            <li>Complete tax return preparation and filing</li>
            <li>Tax documentation organization</li>
            <li>KRA audit support and representation</li>
            <li>One-on-one tax advisory sessions</li>
            <li>Year-round tax planning</li>
        </ul>
        
        <h4>Common Deductions We Identify:</h4>
        <ul>
            <li>Professional expenses and fees</li>
            <li>Travel and vehicle expenses</li>
            <li>Home office deductions</li>
            <li>Education and training expenses</li>
            <li>Healthcare and insurance costs</li>
        </ul>
        
        <h4>Filing Timeline:</h4>
        <p>We prepare and file returns well before the KRA deadline to ensure timely submission and avoid penalties.</p>
        '''
    },
    'vat-filing-etims': {
        'long_description': '''
        <h3>VAT Filing & eTIMS Implementation</h3>
        <p>Complete VAT compliance and eTIMS system implementation to ensure full compliance with KRA requirements.</p>
        
        <h4>VAT Services:</h4>
        <ul>
            <li>VAT return preparation and filing</li>
            <li>Input VAT claim optimization</li>
            <li>VAT refund recovery (including overdue refunds)</li>
            <li>Import VAT management</li>
            <li>VAT compliance audits</li>
        </ul>
        
        <h4>eTIMS Implementation:</h4>
        <ul>
            <li>System setup and configuration</li>
            <li>Staff training on eTIMS operations</li>
            <li>Integration with your business systems</li>
            <li>Daily compliance monitoring</li>
            <li>Technical support and troubleshooting</li>
        </ul>
        
        <h4>Our Expertise:</h4>
        <ul>
            <li>Successfully implemented eTIMS for 200+ businesses</li>
            <li>Expertise in complex imports/exports scenarios</li>
            <li>Knowledge of all VAT rate categories</li>
            <li>Experience with VAT refund recovery processes</li>
            <li>Understanding of special VAT schemes</li>
        </ul>
        
        <h4>Ongoing Support:</h4>
        <ul>
            <li>Monthly VAT reconciliation</li>
            <li>Regular compliance status updates</li>
            <li>System performance monitoring</li>
            <li>Update management as KRA requirements change</li>
        </ul>
        
        <h4>Key Benefits:</h4>
        <ul>
            <li>100% KRA compliance</li>
            <li>Reduced VAT penalties and interest</li>
            <li>Faster VAT refund processing</li>
            <li>Improved business cash flow</li>
            <li>Better financial records and visibility</li>
        </ul>
        '''
    },
    'paye-filing': {
        'long_description': '''
        <h3>PAYE Filing Services</h3>
        <p>Professional PAYE filing and payroll tax management ensuring accurate withholding and timely KRA submission.</p>
        
        <h4>Services Covered:</h4>
        <ul>
            <li>Monthly PAYE calculations and withholding</li>
            <li>Statutory deductions (NSSF, NHIF, housing levy)</li>
            <li>Relief calculations and applications</li>
            <li>PAYE return preparation and filing</li>
            <li>Annual reconciliation and adjustments</li>
        </ul>
        
        <h4>Compliance Management:</h4>
        <ul>
            <li>Monthly PAYE schedule preparation</li>
            <li>Payment tracking and remittance</li>
            <li>Employee records maintenance</li>
            <li>P3 forms and TDS management</li>
            <li>Withholding certificate generation</li>
        </ul>
        
        <h4>Special Situations:</h4>
        <ul>
            <li>Expatriate PAYE management</li>
            <li>Consultant and contractor payments</li>
            <li>Director salary optimization</li>
            <li>Bonus and incentive administration</li>
            <li>Pension and gratuity deductions</li>
        </ul>
        
        <h4>Reporting & Documentation:</h4>
        <ul>
            <li>Monthly PAYE reconciliation statements</li>
            <li>Year-end employee tax certificates</li>
            <li>Annual PAYE verification statements</li>
            <li>Audit trail documentation</li>
        </ul>
        
        <h4>Why Choose Our PAYE Services:</h4>
        <ul>
            <li>Zero penalties with our compliance guarantee</li>
            <li>Accurate calculations reducing employee disputes</li>
            <li>Timely filings avoiding late fees</li>
            <li>Professional record-keeping for audits</li>
            <li>Full KRA communication handling</li>
        </ul>
        '''
    },
    'withholding-tax-management': {
        'long_description': '''
        <h3>Withholding Tax Management</h3>
        <p>Comprehensive withholding tax compliance and management services ensuring full adherence to KRA regulations.</p>
        
        <h4>Withholding Tax Types We Manage:</h4>
        <ul>
            <li>Contractors withholding (5%)</li>
            <li>Professional fees withholding (20%)</li>
            <li>Commission and brokerage withholding (5%)</li>
            <li>Rental income withholding (10%)</li>
            <li>Dividend withholding (15%)</li>
            <li>Management fees withholding (15%)</li>
        </ul>
        
        <h4>Services Provided:</h4>
        <ul>
            <li>Withholding calculations for various payment types</li>
            <li>WHTT return preparation and filing</li>
            <li>Payment tracking and remittance management</li>
            <li>Crediting documentation for vendors</li>
            <li>Compliance verification</li>
        </ul>
        
        <h4>Common Scenarios:</h4>
        <ul>
            <li>Managing contractors and suppliers</li>
            <li>Processing professional service payments</li>
            <li>Real estate property rentals</li>
            <li>Dividend and investment payments</li>
            <li>Third-party service provider payments</li>
        </ul>
        
        <h4>Monthly Management:</h4>
        <ul>
            <li>Invoice review and withholding assessment</li>
            <li>Calculation and documentation</li>
            <li>Payment schedule preparation</li>
            <li>Vendor communication and crediting</li>
            <li>Records reconciliation</li>
        </ul>
        
        <h4>Key Advantages:</h4>
        <ul>
            <li>Reduced compliance penalties</li>
            <li>Better vendor relationships through transparency</li>
            <li>Accurate tax position reporting</li>
            <li>Improved cash flow management</li>
            <li>Simplified audit processes</li>
        </ul>
        '''
    },
    'bookkeeping-financial-statements': {
        'long_description': '''
        <h3>Bookkeeping & Financial Statements</h3>
        <p>Professional bookkeeping services and comprehensive financial statement preparation providing clear visibility into your business finances.</p>
        
        <h4>Bookkeeping Services:</h4>
        <ul>
            <li>Daily transaction recording</li>
            <li>Invoice and receipt management</li>
            <li>Expense categorization and coding</li>
            <li>Bank reconciliation (monthly)</li>
            <li>Trial balance preparation</li>
            <li>Ledger management</li>
        </ul>
        
        <h4>Financial Statements Prepared:</h4>
        <ul>
            <li>Income Statement (Profit & Loss)</li>
            <li>Balance Sheet</li>
            <li>Cash Flow Statement</li>
            <li>Statement of Changes in Equity</li>
            <li>Financial notes and disclosures</li>
        </ul>
        
        <h4>Data Entry & Processing:</h4>
        <ul>
            <li>Invoice data entry and tracking</li>
            <li>Expense receipt processing</li>
            <li>Payroll data compilation</li>
            <li>Bank statement reconciliation</li>
            <li>Year-end adjustments</li>
        </ul>
        
        <h4>Analysis & Reporting:</h4>
        <ul>
            <li>Monthly financial summaries</li>
            <li>Key performance ratio analysis</li>
            <li>Cash flow projections</li>
            <li>Variance analysis and insights</li>
            <li>Management reporting</li>
        </ul>
        
        <h4>Business Benefits:</h4>
        <ul>
            <li>Clear understanding of business profitability</li>
            <li>Better decision-making with accurate data</li>
            <li>Simplified tax filing process</li>
            <li>Bank and investor confidence</li>
            <li>Early identification of financial issues</li>
        </ul>
        
        <h4>System Options:</h4>
        <ul>
            <li>QuickBooks Online integration</li>
            <li>Xero accounting software</li>
            <li>SAP integration for large businesses</li>
            <li>Custom spreadsheet solutions for smaller entities</li>
        </ul>
        '''
    },
    'resolving-vat-errors': {
        'long_description': '''
        <h3>Resolving Errors in VAT Returns</h3>
        <p>Expert resolution of VAT return discrepancies, errors, and omissions ensuring KRA compliance and recovering lost refunds.</p>
        
        <h4>Common VAT Error Types We Fix:</h4>
        <ul>
            <li>Incorrect input VAT claims</li>
            <li>Computational errors in VAT calculations</li>
            <li>Overstated output VAT</li>
            <li>Incorrect filing deadlines</li>
            <li>Missing documentation for claims</li>
            <li>eTIMS data inconsistencies</li>
        </ul>
        
        <h4>Our Correction Process:</h4>
        <ul>
            <li>Comprehensive error audit and identification</li>
            <li>Root cause analysis</li>
            <li>Documentation review and preparation</li>
            <li>Amendment filing preparation</li>
            <li>KRA communication and negotiation</li>
            <li>Follow-up and monitoring</li>
        </ul>
        
        <h4>Recovery Services:</h4>
        <ul>
            <li>Overpaid VAT refund recovery</li>
            <li>Wrongly denied refund appeals</li>
            <li>Missed refund claims recovery</li>
            <li>Large refund claims (500k+)</li>
            <li>Multi-year error corrections</li>
        </ul>
        
        <h4>Documentation We Provide:</h4>
        <ul>
            <li>Error analysis report</li>
            <li>Corrected VAT schedules</li>
            <li>Supporting documentation package</li>
            <li>Amendment letter to KRA</li>
            <li>Refund claim justification</li>
        </ul>
        
        <h4>Results Achieved:</h4>
        <ul>
            <li>Average VAT recovery: Ksh 200k - 1M+</li>
            <li>80% amendment acceptance rate</li>
            <li>Reduced penalties through corrections</li>
            <li>Improved compliance going forward</li>
        </ul>
        '''
    },
    'legacy-ledger-correction': {
        'long_description': '''
        <h3>Migrated Legacy Ledger Correction</h3>
        <p>Specialized services for resolving issues with legacy account migrations and ensuring system accuracy after data transfers.</p>
        
        <h4>Migration Issues We Resolve:</h4>
        <ul>
            <li>Data mapping errors during migration</li>
            <li>Missing or incomplete transactions</li>
            <li>Account balance discrepancies</li>
            <li>Duplicate entries</li>
            <li>Currency conversion errors</li>
            <li>Date and period inconsistencies</li>
        </ul>
        
        <h4>System Migrations We Support:</h4>
        <ul>
            <li>Legacy systems to QuickBooks</li>
            <li>Manual books to Xero</li>
            <li>Old accounting software to cloud systems</li>
            <li>Spreadsheet-based to formal accounting systems</li>
            <li>International to local system transfers</li>
        </ul>
        
        <h4>Correction Process:</h4>
        <ul>
            <li>Source data validation and reconciliation</li>
            <li>Target system audit and verification</li>
            <li>Discrepancy identification and analysis</li>
            <li>Corrective entry preparation</li>
            <li>Balance rebuilding and validation</li>
            <li>Post-correction verification</li>
        </ul>
        
        <h4>Deliverables:</h4>
        <ul>
            <li>Migration audit report</li>
            <li>Discrepancy analysis with root causes</li>
            <li>Corrective journal entries</li>
            <li>Reconciliation schedules</li>
            <li>Post-migration validation certificate</li>
        </ul>
        
        <h4>Benefits:</h4>
        <ul>
            <li>Accurate financial records for tax filing</li>
            <li>Reliable data for decision-making</li>
            <li>Audit-ready documentation</li>
            <li>Clean systems for future operations</li>
            <li>Reduced future accounting issues</li>
        </ul>
        '''
    },
    'kra-audits-objections': {
        'long_description': '''
        <h3>KRA Audits, Objections and Appeals</h3>
        <p>Expert representation and professional support throughout the KRA audit process, objection filing, and appeals procedures.</p>
        
        <h4>Audit Support Services:</h4>
        <ul>
            <li>KRA audit notification analysis</li>
            <li>Documentation preparation and organization</li>
            <li>Records compilation and verification</li>
            <li>Risk assessment and strategy</li>
            <li>Professional representation during audits</li>
            <li>Correspondence management</li>
        </ul>
        
        <h4>Objection Services:</h4>
        <ul>
            <li>Assessment review and analysis</li>
            <li>Objection grounds identification</li>
            <li>Professional objection letter preparation</li>
            <li>Supporting documentation compilation</li>
            <li>KRA objection filing</li>
            <li>Follow-up communication</li>
        </ul>
        
        <h4>Appeals Process:</h4>
        <ul>
            <li>Tax Disputes Tribunal representation</li>
            <li>Appeal case preparation</li>
            <li>Evidence organization and presentation</li>
            <li>Hearing preparation and strategy</li>
            <li>Professional testimony coordination</li>
        </ul>
        
        <h4>Audit Types We Handle:</h4>
        <ul>
            <li>Income tax audits (individuals and companies)</li>
            <li>VAT compliance audits</li>
            <li>Payroll tax audits</li>
            <li>Withholding tax audits</li>
            <li>General compliance audits</li>
            <li>Sector-specific audits</li>
        </ul>
        
        <h4>Our Track Record:</h4>
        <ul>
            <li>70% successful objection outcomes</li>
            <li>Average tax reduction: 30-50%</li>
            <li>Reduced penalties through professional representation</li>
            <li>Maintained client relationships with KRA</li>
        </ul>
        
        <h4>Why Professional Representation Matters:</h4>
        <ul>
            <li>Expert knowledge of tax law and regulations</li>
            <li>Strategic objection and appeal positioning</li>
            <li>Reduced emotional stress during audits</li>
            <li>Professional credibility with KRA officials</li>
            <li>Faster resolution timelines</li>
        </ul>
        '''
    },
    'itax-ledger-correction': {
        'long_description': '''
        <h3>Correction of Errors in iTAX Ledgers</h3>
        <p>Specialized resolution of iTAX ledger errors and discrepancies ensuring accurate tax records with KRA.</p>
        
        <h4>Common iTAX Errors:</h4>
        <ul>
            <li>Duplicate transaction entries</li>
            <li>Incorrect income categorization</li>
            <li>Wrong deduction classifications</li>
            <li>Missing expense documentation</li>
            <li>Relief claim errors</li>
            <li>Year-end balance discrepancies</li>
            <li>PIN registration issues</li>
        </ul>
        
        <h4>Error Resolution Process:</h4>
        <ul>
            <li>iTAX account audit and analysis</li>
            <li>Error identification and documentation</li>
            <li>Correction request preparation</li>
            <li>Supporting evidence compilation</li>
            <li>KRA correction submission</li>
            <li>Status tracking and confirmation</li>
        </ul>
        
        <h4>Services Provided:</h4>
        <ul>
            <li>iTAX data reconciliation</li>
            <li>Pin and taxpayer data correction</li>
            <li>Income and expense adjustments</li>
            <li>Balancing item corrections</li>
            <li>Penalty reduction negotiations</li>
            <li>Future filing guidance</li>
        </ul>
        
        <h4>Correction Categories:</h4>
        <ul>
            <li>Data entry errors</li>
            <li>System glitches and technical errors</li>
            <li>Filing mistakes and omissions</li>
            <li>Amendment and adjustment errors</li>
            <li>Relief claims adjustments</li>
        </ul>
        
        <h4>Documentation Prepared:</h4>
        <ul>
            <li>Error audit report</li>
            <li>Corrected schedules and forms</li>
            <li>Supporting documentation package</li>
            <li>Letter to KRA with correction request</li>
            <li>Follow-up communication</li>
        </ul>
        
        <h4>Outcomes:</h4>
        <ul>
            <li>Accurate iTAX records for future compliance</li>
            <li>Improved credibility with KRA</li>
            <li>Reduced future audit risk</li>
            <li>Accurate refund calculations</li>
            <li>Peace of mind regarding tax position</li>
        </ul>
        '''
    },
    'kra-pending-applications': {
        'long_description': '''
        <h3>Closing Out on Applications Pending at the KRA</h3>
        <p>Expert assistance in resolving and closing out applications pending with KRA, accelerating approval processes.</p>
        
        <h4>Typical Pending Applications:</h4>
        <ul>
            <li>VAT refund claims (sometimes delayed 6-12 months)</li>
            <li>Import duty refunds</li>
            <li>Exemption certifications</li>
            <li>Special schemes approvals</li>
            <li>Relief applications</li>
            <li>Deferment or installment requests</li>
            <li>Tax waiver or amnesty applications</li>
        </ul>
        
        <h4>Resolution Services:</h4>
        <ul>
            <li>Application status tracking with KRA</li>
            <li>Missing documentation identification</li>
            <li>Supporting evidence compilation</li>
            <li>Professional follow-up communication</li>
            <li>KRA official liaison and negotiation</li>
            <li>Expedited processing advocacy</li>
        </ul>
        
        <h4>Our Process:</h4>
        <ul>
            <li>Detailed application file review</li>
            <li>Status and delay cause identification</li>
            <li>Gap analysis and problem solving</li>
            <li>Document remediation if needed</li>
            <li>Formal KRA follow-up letters</li>
            <li>Regular status updates</li>
            <li>Approval facilitation</li>
        </ul>
        
        <h4>Results:</h4>
        <ul>
            <li>Average resolution time: 30-60 days</li>
            <li>85% success rate on stalled applications</li>
            <li>Improved cash flow from recovered refunds</li>
            <li>Reduced stress through professional handling</li>
        </ul>
        
        <h4>Financial Impact:</h4>
        <p>For pending VAT refunds averaging Ksh 300k, our assistance typically results in faster recovery worth significantly more than our service fees.</p>
        
        <h4>Why Applications Get Stuck:</h4>
        <ul>
            <li>Missing or incomplete documentation</li>
            <li>System delays within KRA</li>
            <li>Incorrect filing procedures</li>
            <li>Administrative backlogs</li>
            <li>Insufficient following up</li>
        </ul>
        '''
    },
    'corporate-tax-planning': {
        'long_description': '''
        <h3>Corporate Tax Planning & More</h3>
        <p>Comprehensive corporate tax planning and related services including restructuring, optimization, and strategic business advisory.</p>
        
        <h4>Corporate Tax Planning Services:</h4>
        <ul>
            <li>Year-round tax planning and optimization</li>
            <li>Tax-efficient business structuring</li>
            <li>Dividend policy optimization</li>
            <li>Capital structure planning</li>
            <li>Loss utilization strategies</li>
            <li>Deduction and relief maximization</li>
        </ul>
        
        <h4>Business Restructuring Services:</h4>
        <ul>
            <li>Business registration and licensing</li>
            <li>Company incorporation consulting</li>
            <li>Partnership to company conversion</li>
            <li>Acquisition and merger tax planning</li>
            <li>Business succession planning</li>
            <li>Shareholder agreement structuring</li>
        </ul>
        
        <h4>Strategic Services Include:</h4>
        <ul>
            <li>Transfer pricing compliance</li>
            <li>Related party transaction structuring</li>
            <li>Loan agreement documentation</li>
            <li>Royalty arrangements</li>
            <li>Management fee optimization</li>
            <li>Inter-company pricing</li>
        </ul>
        
        <h4>Advanced Planning:</h4>
        <ul>
            <li>Holding company structures</li>
            <li>Investment fund structuring</li>
            <li>Real estate investment tax planning</li>
            <li>Technology business optimization</li>
            <li>Manufacturing sector planning</li>
            <li>Export business structures</li>
        </ul>
        
        <h4>Financial Services:</h4>
        <ul>
            <li>Financial statement preparation and analysis</li>
            <li>Annual compliance reporting</li>
            <li>Management financial reporting</li>
            <li>Audit coordination</li>
            <li>Regulatory compliance</li>
            <li>Fraud prevention and detection</li>
        </ul>
        
        <h4>Strategic Benefits:</h4>
        <ul>
            <li>Tax savings of 15-35% through strategic planning</li>
            <li>Improved business valuation</li>
            <li>Simplified succession and exit strategies</li>
            <li>Enhanced shareholder value</li>
            <li>Reduced regulatory and audit risk</li>
            <li>Competitive business positioning</li>
        </ul>
        
        <h4>Industries We Specialize In:</h4>
        <ul>
            <li>Technology and software</li>
            <li>Manufacturing and production</li>
            <li>Real estate and property</li>
            <li>Retail and e-commerce</li>
            <li>Professional services</li>
            <li>Agriculture and agribusiness</li>
            <li>Import/export trading</li>
        </ul>
        '''
    },
}

# FAQs for each service
faqs_data = {
    'tax-health-checks': [
        {
            'question': 'Should I get a tax health check if my business is running well?',
            'answer': 'Yes, absolutely. A tax health check helps identify hidden compliance risks and optimization opportunities that could save you money even if revenue is strong.'
        },
        {
            'question': 'How long does a tax health check take?',
            'answer': 'Typically 1-2 weeks depending on your business complexity and document availability. We\'ll give you a timeline after initial consultation.'
        },
        {
            'question': 'What if the health check finds problems?',
            'answer': 'We don\'t just identify problems - we provide solutions. We\'ll recommend corrective actions and help implement them to bring you into full compliance.'
        },
    ],
    'strategic-tax-advisory': [
        {
            'question': 'Can strategic tax planning really save money?',
            'answer': 'Yes. Through legitimate tax planning strategies, most businesses save between 10-30% of their tax liabilities annually.'
        },
        {
            'question': 'Is tax planning legal?',
            'answer': 'Absolutely. Tax planning uses legal strategies within KRA regulations. Tax evasion is illegal; tax planning is smart business.'
        },
        {
            'question': 'When should I start tax planning?',
            'answer': 'Ideally at the beginning of your financial year or during business planning season, but we can implement strategies at any time.'
        },
    ],
    'income-tax-filing-advisory': [
        {
            'question': 'What happens if I file my taxes late?',
            'answer': 'Late filing typically results in penalties. We handle filing before the deadline to avoid these charges.'
        },
        {
            'question': 'How do you know what deductions I can claim?',
            'answer': 'We review all your business and personal expenses against KRA regulations to identify legitimate deductions.'
        },
        {
            'question': 'Do I need to keep documents if I file with you?',
            'answer': 'Yes, keep all supporting documents for 5 years in case of KRA inquiry. We keep copies too for our records.'
        },
    ],
    'vat-filing-etims': [
        {
            'question': 'What is eTIMS and why do I need it?',
            'answer': 'eTIMS is KRA\'s electronic tax invoice management system. It\'s mandatory for VAT-registered businesses and helps ensure compliance.'
        },
        {
            'question': 'Can I recover VAT on all my purchases?',
            'answer': 'Most business purchases include recoverable VAT, but some items (like fuel and some services) have restrictions. We identify what you can legally recover.'
        },
        {
            'question': 'Why are my VAT refunds delayed?',
            'answer': 'Delays often result from incomplete documentation or system issues. We identify the cause and work to get your refund processed.'
        },
    ],
    'paye-filing': [
        {
            'question': 'What happens if I don\'t file PAYE on time?',
            'answer': 'Late PAYE filing results in penalties and potential audit. We make sure files are submitted before deadlines.'
        },
        {
            'question': 'Do I have to pay PAYE every month?',
            'answer': 'Yes, for most employers. Monthly PAYE withholding is mandatory and must be paid to KRA by the 20th of following month.'
        },
        {
            'question': 'What if I have expatriate employees?',
            'answer': 'We handle expatriate PAYE with special considerations for foreign tax relief, non-resident treatment, and employment rules.'
        },
    ],
}

print("Updating services with detailed long descriptions and FAQs...\n")

for slug, details in services_data.items():
    try:
        service = Service.objects.get(slug=slug)
        service.long_description = details['long_description']
        service.save()
        print(f"✓ Updated: {service.name}")
    except Service.DoesNotExist:
        print(f"✗ Not found: {slug}")

# Add FAQs
for slug, faq_list in faqs_data.items():
    try:
        service = Service.objects.get(slug=slug)
        # Clear existing FAQs
        service.faqs.all().delete()
        # Add new FAQs
        for idx, faq_data in enumerate(faq_list):
            ServiceFAQ.objects.create(
                service=service,
                question=faq_data['question'],
                answer=faq_data['answer'],
                order=idx
            )
        print(f"✓ Added {len(faq_list)} FAQs to: {service.name}")
    except Service.DoesNotExist:
        print(f"✗ Not found for FAQs: {slug}")

print("\nDone! Services updated with detailed information.")
