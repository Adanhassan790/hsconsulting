from django.core.management.base import BaseCommand
from datetime import date
from apps.appointments.models import TaxDeadline


class Command(BaseCommand):
    help = 'Populate Kenyan KRA tax deadlines for 2026'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing deadlines...')
        TaxDeadline.objects.all().delete()

        deadlines = []

        # ------------------------------------------------------------------ #
        # PAYE — due by 9th of the following month                           #
        # ------------------------------------------------------------------ #
        paye_months = [
            (date(2026, 1, 9),  'December 2025'),
            (date(2026, 2, 9),  'January 2026'),
            (date(2026, 3, 9),  'February 2026'),
            (date(2026, 4, 9),  'March 2026'),
            (date(2026, 5, 9),  'April 2026'),
            (date(2026, 6, 9),  'May 2026'),
            (date(2026, 7, 9),  'June 2026'),
            (date(2026, 8, 9),  'July 2026'),
            (date(2026, 9, 9),  'August 2026'),
            (date(2026, 10, 9), 'September 2026'),
            (date(2026, 11, 9), 'October 2026'),
            (date(2026, 12, 9), 'November 2026'),
        ]
        for due_date, period in paye_months:
            deadlines.append(TaxDeadline(
                name=f'PAYE — {period}',
                description=(
                    f'Pay As You Earn (PAYE) tax remittance and returns for {period}. '
                    'Employers must deduct and remit PAYE to KRA by the 9th of the '
                    'following month. File via iTax (www.itax.kra.go.ke).'
                ),
                deadline_date=due_date,
                deadline_type='paye',
                recurring=True,
            ))

        # ------------------------------------------------------------------ #
        # VAT — monthly returns due 20th of following month                  #
        # ------------------------------------------------------------------ #
        vat_months = [
            (date(2026, 1, 20),  'December 2025'),
            (date(2026, 2, 20),  'January 2026'),
            (date(2026, 3, 20),  'February 2026'),
            (date(2026, 4, 20),  'March 2026'),
            (date(2026, 5, 20),  'April 2026'),
            (date(2026, 6, 20),  'May 2026'),
            (date(2026, 7, 20),  'June 2026'),
            (date(2026, 8, 20),  'July 2026'),
            (date(2026, 9, 20),  'August 2026'),
            (date(2026, 10, 20), 'September 2026'),
            (date(2026, 11, 20), 'October 2026'),
            (date(2026, 12, 20), 'November 2026'),
        ]
        for due_date, period in vat_months:
            deadlines.append(TaxDeadline(
                name=f'VAT Returns — {period}',
                description=(
                    f'Monthly VAT (Value Added Tax) return submission for {period}. '
                    'VAT-registered taxpayers must file returns and pay any VAT due '
                    'by the 20th of the following month via iTax. Rate: 16% standard.'
                ),
                deadline_date=due_date,
                deadline_type='vat',
                recurring=True,
            ))

        # ------------------------------------------------------------------ #
        # Withholding Tax — 20th of following month                          #
        # ------------------------------------------------------------------ #
        wht_months = [
            (date(2026, 1, 20),  'December 2025'),
            (date(2026, 2, 20),  'January 2026'),
            (date(2026, 3, 20),  'February 2026'),
            (date(2026, 4, 20),  'March 2026'),
            (date(2026, 5, 20),  'April 2026'),
            (date(2026, 6, 20),  'May 2026'),
            (date(2026, 7, 20),  'June 2026'),
            (date(2026, 8, 20),  'July 2026'),
            (date(2026, 9, 20),  'August 2026'),
            (date(2026, 10, 20), 'September 2026'),
            (date(2026, 11, 20), 'October 2026'),
            (date(2026, 12, 20), 'November 2026'),
        ]
        for due_date, period in wht_months:
            deadlines.append(TaxDeadline(
                name=f'Withholding Tax — {period}',
                description=(
                    f'Withholding Tax (WHT) remittance and certificate issuance for {period}. '
                    'Applies to payments such as dividends, interest, royalties, management '
                    'fees, rent, and contractor payments. Remit via iTax by the 20th.'
                ),
                deadline_date=due_date,
                deadline_type='other',
                recurring=True,
            ))

        # ------------------------------------------------------------------ #
        # Instalment Tax (Advance Tax) — quarterly for Dec 31 year-end       #
        # ------------------------------------------------------------------ #
        deadlines += [
            TaxDeadline(
                name='Instalment Tax — 1st Instalment (25%)',
                description=(
                    'First instalment of advance corporate tax for companies with '
                    '31 December year-end. Pay 25% of the estimated annual tax liability '
                    'or prior year tax (whichever is higher) via iTax.'
                ),
                deadline_date=date(2026, 4, 20),
                deadline_type='income_tax',
                recurring=True,
            ),
            TaxDeadline(
                name='Instalment Tax — 2nd Instalment (50% cumulative)',
                description=(
                    'Second instalment of advance corporate tax. Cumulative payment '
                    'should reach 50% of the estimated annual tax liability by this date. '
                    'Pay via iTax on Form ITR-1.'
                ),
                deadline_date=date(2026, 6, 20),
                deadline_type='income_tax',
                recurring=True,
            ),
            TaxDeadline(
                name='Instalment Tax — 3rd Instalment (75% cumulative)',
                description=(
                    'Third instalment of advance corporate tax. Cumulative payment '
                    'should reach 75% of the estimated annual tax liability by this date. '
                    'Failure to pay instalments attracts interest at 2% per month.'
                ),
                deadline_date=date(2026, 9, 20),
                deadline_type='income_tax',
                recurring=True,
            ),
            TaxDeadline(
                name='Instalment Tax — 4th Instalment (100% cumulative)',
                description=(
                    'Final instalment of advance corporate tax for the year. '
                    'Total cumulative payments must cover 100% of the estimated annual '
                    'tax liability. Balance due with annual return by 30 June 2027.'
                ),
                deadline_date=date(2026, 12, 20),
                deadline_type='income_tax',
                recurring=True,
            ),
        ]

        # ------------------------------------------------------------------ #
        # Annual Income Tax Returns                                           #
        # ------------------------------------------------------------------ #
        deadlines += [
            TaxDeadline(
                name='Individual Income Tax Return (ITR) — FY 2025',
                description=(
                    'Annual income tax self-assessment return for individuals for '
                    'financial year 2025. Includes employment income, business income, '
                    'rental income, and investment income. File and pay any balance '
                    'due via iTax. Penalty for late filing: KES 2,000 or 5% of tax due.'
                ),
                deadline_date=date(2026, 6, 30),
                deadline_type='income_tax',
                recurring=True,
            ),
            TaxDeadline(
                name='Corporation Tax Return — FY 2025 (Dec 31 year-end)',
                description=(
                    'Annual corporation tax return for companies whose financial year '
                    'ended 31 December 2025. File Form ITR-2P via iTax and pay any '
                    'balance due. Corporate tax rate: 30% (resident), 37.5% (non-resident). '
                    'Penalty for late filing: 5% of tax due + 2% per month on unpaid balance.'
                ),
                deadline_date=date(2026, 6, 30),
                deadline_type='income_tax',
                recurring=True,
            ),
            TaxDeadline(
                name='Turnover Tax (TOT) Annual Return — FY 2025',
                description=(
                    'Annual Turnover Tax return for small businesses with annual gross '
                    'turnover between KES 500,000 and KES 50,000,000. Rate: 3% of gross '
                    'turnover. File via iTax. Note: TOT is due monthly (20th of following '
                    'month) in addition to this annual reconciliation.'
                ),
                deadline_date=date(2026, 6, 30),
                deadline_type='income_tax',
                recurring=True,
            ),
            TaxDeadline(
                name='Rental Income Tax Return — FY 2025',
                description=(
                    'Annual tax return for residential rental income. Residential rental '
                    'income is taxed at 10% of gross rent received (monthly installments '
                    'due by 20th of following month). File annual return by 30 June. '
                    'Applies to landlords earning rental income from residential property.'
                ),
                deadline_date=date(2026, 6, 30),
                deadline_type='income_tax',
                recurring=True,
            ),
        ]

        # ------------------------------------------------------------------ #
        # NSSF (National Social Security Fund) — 9th of month                #
        # ------------------------------------------------------------------ #
        nssf_months = [
            (date(2026, 1, 9),  'December 2025'),
            (date(2026, 2, 9),  'January 2026'),
            (date(2026, 3, 9),  'February 2026'),
            (date(2026, 4, 9),  'March 2026'),
            (date(2026, 5, 9),  'April 2026'),
            (date(2026, 6, 9),  'May 2026'),
            (date(2026, 7, 9),  'June 2026'),
            (date(2026, 8, 9),  'July 2026'),
            (date(2026, 9, 9),  'August 2026'),
            (date(2026, 10, 9), 'September 2026'),
            (date(2026, 11, 9), 'October 2026'),
            (date(2026, 12, 9), 'November 2026'),
        ]
        for due_date, period in nssf_months:
            deadlines.append(TaxDeadline(
                name=f'NSSF Contributions — {period}',
                description=(
                    f'National Social Security Fund contributions for {period}. '
                    'Employer contributes KES 200/month per employee (Tier I: KES 72, '
                    'Tier II: KES 128) under NSSF Act 2013 pending court outcome. '
                    'Remit alongside PAYE via the NSSF employer portal.'
                ),
                deadline_date=due_date,
                deadline_type='other',
                recurring=True,
            ))

        created = TaxDeadline.objects.bulk_create(deadlines)
        self.stdout.write(self.style.SUCCESS(
            f'[OK] Successfully created {len(created)} KRA tax deadlines for 2026'
        ))
