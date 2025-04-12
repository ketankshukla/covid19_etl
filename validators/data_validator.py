"""
Module for validating data quality using Great Expectations-like approach.
"""
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class SimpleValidator:
    """
    A simple data validator inspired by Great Expectations.
    
    This is a simplified version that implements basic validation rules
    without requiring the full Great Expectations library.
    """
    
    def __init__(self, df):
        """
        Initialize validator with a DataFrame.
        
        Args:
            df (pandas.DataFrame): The DataFrame to validate
        """
        self.df = df
        self.validation_results = []
    
    def expect_column_to_exist(self, column):
        """Check if a column exists in the DataFrame."""
        result = column in self.df.columns
        self._add_result(f"Column '{column}' exists", result)
        return result
    
    def expect_column_values_to_not_be_null(self, column):
        """Check if a column has no null values."""
        if not self.expect_column_to_exist(column):
            return False
        
        null_count = self.df[column].isna().sum()
        result = null_count == 0
        self._add_result(f"Column '{column}' has no null values", result, 
                         details=f"{null_count} null values found" if not result else "")
        return result
    
    def expect_column_values_to_be_between(self, column, min_value, max_value):
        """Check if all values in a column are between min_value and max_value."""
        if not self.expect_column_to_exist(column):
            return False
        
        # Filter out null values for the check
        values = self.df[column].dropna()
        
        if len(values) == 0:
            self._add_result(f"Column '{column}' values between {min_value} and {max_value}", False,
                            details="Column has no non-null values")
            return False
        
        min_actual = values.min()
        max_actual = values.max()
        result = (min_actual >= min_value) and (max_actual <= max_value)
        
        self._add_result(f"Column '{column}' values between {min_value} and {max_value}", result,
                         details=f"Range is {min_actual} to {max_actual}" if not result else "")
        return result
    
    def expect_column_values_to_be_of_type(self, column, expected_type):
        """Check if all values in a column are of the expected type."""
        if not self.expect_column_to_exist(column):
            return False
        
        # Map pandas/numpy types to Python types for easier comparison
        type_mapping = {
            'int': (pd.api.types.is_integer_dtype, int),
            'float': (pd.api.types.is_float_dtype, float),
            'str': (pd.api.types.is_string_dtype, str),
            'datetime': (pd.api.types.is_datetime64_dtype, 'datetime')
        }
        
        if expected_type in type_mapping:
            type_check_func, _ = type_mapping[expected_type]
            result = type_check_func(self.df[column])
        else:
            # Fall back to Python type checking if pandas type check not available
            result = all(isinstance(x, expected_type) for x in self.df[column].dropna())
        
        self._add_result(f"Column '{column}' values are of type {expected_type}", result)
        return result
    
    def expect_column_values_to_be_unique(self, column):
        """Check if all values in a column are unique."""
        if not self.expect_column_to_exist(column):
            return False
        
        duplicate_count = self.df[column].duplicated().sum()
        result = duplicate_count == 0
        
        self._add_result(f"Column '{column}' values are unique", result,
                         details=f"{duplicate_count} duplicates found" if not result else "")
        return result
    
    def _add_result(self, expectation, success, details=""):
        """Add a validation result to the results list."""
        self.validation_results.append({
            'expectation': expectation,
            'success': success,
            'details': details
        })
    
    def get_validation_results(self):
        """Get all validation results."""
        return self.validation_results
    
    def validate(self):
        """Get summary of validation results."""
        total = len(self.validation_results)
        success_count = sum(1 for r in self.validation_results if r['success'])
        
        logger.info(f"Validation complete: {success_count}/{total} expectations passed")
        
        if success_count < total:
            # Log failed validations
            for result in self.validation_results:
                if not result['success']:
                    details = f" - {result['details']}" if result['details'] else ""
                    logger.warning(f"Failed: {result['expectation']}{details}")
        
        return success_count == total

def validate_covid_data(df):
    """
    Validate COVID-19 data using common expectations.
    
    Args:
        df (pandas.DataFrame): DataFrame to validate
        
    Returns:
        bool: True if all validations pass, False otherwise
    """
    logger.info("Starting data validation")
    
    try:
        validator = SimpleValidator(df)
        
        # Common columns to check
        date_column = next((col for col in df.columns if 'date' in col.lower()), None)
        location_column = next((col for col in df.columns if any(loc in col.lower() for loc in ['region', 'location', 'state'])), None)
        
        # Basic validation checks
        if date_column:
            validator.expect_column_to_exist(date_column)
            validator.expect_column_values_to_not_be_null(date_column)
        
        if location_column:
            validator.expect_column_to_exist(location_column)
            validator.expect_column_values_to_not_be_null(location_column)
        
        # Check numeric columns for reasonable ranges
        numeric_columns = df.select_dtypes(include=['number']).columns
        for col in numeric_columns:
            if 'rate' in col.lower() or 'percentage' in col.lower():
                validator.expect_column_values_to_be_between(col, 0, 100)
            elif any(term in col.lower() for term in ['cases', 'deaths', 'tests', 'vaccinations']):
                validator.expect_column_values_to_be_between(col, 0, float('inf'))
        
        # Run validation and return result
        return validator.validate()
    
    except Exception as e:
        logger.error(f"Error validating data: {e}")
        return False